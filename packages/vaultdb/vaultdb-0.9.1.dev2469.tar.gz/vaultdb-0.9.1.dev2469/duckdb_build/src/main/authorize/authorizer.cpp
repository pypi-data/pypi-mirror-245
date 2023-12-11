#include "duckdb/main/authorizer.hpp"

#include "duckdb/catalog/catalog_entry/fortress_catalog_entry.hpp"
#include "duckdb/catalog/catalog_entry/role_catalog_entry.hpp"
#include "duckdb/catalog/catalog_entry/scalar_function_catalog_entry.hpp"
#include "duckdb/catalog/catalog_entry/table_catalog_entry.hpp"
#include "duckdb/catalog/catalog_search_path.hpp"
#include "duckdb/main/client_context.hpp"
#include "duckdb/main/config.hpp"
#include "duckdb/main/table_description.hpp"
#include "duckdb/parser/expression/conjunction_expression.hpp"
#include "duckdb/parser/expression/star_expression.hpp"
#include "duckdb/parser/parser.hpp"
#include "duckdb/parser/statement/vacuum_statement.hpp"
#include "duckdb/parser/tableref/joinref.hpp"
#include "duckdb/planner/binder.hpp"
#include "duckdb/planner/constraints/list.hpp"
#include "duckdb/planner/expression.hpp"
#include "duckdb/planner/expression/bound_constant_expression.hpp"
#include "duckdb/planner/expression_binder/check_binder.hpp"

namespace duckdb {

Authorizer::Authorizer(ClientContext &context_p, string role) : context(context_p), role(role) {
}

void Authorizer::Role(const string &changed_role) {
	if (current_role && changed_role == current_role->name)
		return;

	bool new_transaction = !context.transaction.HasActiveTransaction();
	if (new_transaction)
		context.transaction.BeginTransaction();

	for (auto table : constrained_tables) {
		auto schema_name = table.second.substr(0, table.second.find("."));
		auto table_name = table.second.substr(table.second.find(".") + 1, table.second.length() - 1);
		auto table_entry = Catalog::GetEntry<TableCatalogEntry>(context, INVALID_CATALOG, schema_name, table_name,
		                                                        OnEntryNotFound::THROW_EXCEPTION);
		table_entry->fortress_constraints.clear();
	}
	constrained_tables.clear();
	string active_role = role;
	if (changed_role.empty()) {
		current_role = nullptr;
	} else {
		active_role = changed_role;
		if (active_role == INTERNAL_ROLE) {
			current_role = make_uniq<CreateRoleInfo>();
			current_role->superuser = true;
			current_role->login = false;
			current_role->schema = SECURITY_SCHEMA;
			current_role->name = INTERNAL_ROLE;
		} else {
			auto role_entry = Catalog::GetEntry<RoleCatalogEntry>(context, INVALID_CATALOG, SECURITY_SCHEMA,
			                                                      active_role, OnEntryNotFound::RETURN_NULL);
			if (role_entry) {
				auto role_copy = role_entry->info->CopyRole();
				current_role = std::move(role_copy);
			}
		}
	}

	if (new_transaction)
		context.transaction.Commit();
}

shared_ptr<CreateRoleInfo> Authorizer::GetCurrentRole() {
	if (!current_role && !role.empty())
		Role(role);

	if (current_role)
		return current_role;

	throw PermissionException("Please connect with valid role.");
}

unique_ptr<ParsedExpression> Authorizer::AddFortressExpression(TableRef &tableref,
                                                               unique_ptr<ParsedExpression> where_clause,
                                                               duckdb_libpgquery::PGPrivilegeOption privilege_option) {
	if (GetCurrentRole()->superuser)
		return std::move(where_clause);

	switch (tableref.type) {
	case TableReferenceType::BASE_TABLE: {
		auto &basetable = (BaseTableRef &)tableref;

		unique_ptr<ParsedExpression> result;

		bool new_transaction = !context.transaction.HasActiveTransaction();
		if (new_transaction)
			context.transaction.BeginTransaction();

		auto table_entry = Catalog::GetEntry<TableCatalogEntry>(context, INVALID_CATALOG, basetable.schema_name,
		                                                        basetable.table_name, OnEntryNotFound::THROW_EXCEPTION);
		if (table_entry->fortress.size() == 0) {
			if (new_transaction)
				context.transaction.Commit();
			return std::move(where_clause);
		}

		auto it = GetCurrentRole()->privileges.find(CatalogType::FORTRESS_ENTRY);
		bool add_or = false;
		auto alias = basetable.alias;
		for (auto privilege : table_entry->fortress) {
			auto fortress_entry = Catalog::GetEntry<FortressCatalogEntry>(context, INVALID_CATALOG, SECURITY_SCHEMA,
			                                                              privilege, OnEntryNotFound::RETURN_NULL);
			if (!fortress_entry || !fortress_entry->isLocked())
				continue;
			auto exp = fortress_entry->complement_expression->Copy();
			auto conjuctiontype = ExpressionType::CONJUNCTION_AND;
			if (it != GetCurrentRole()->privileges.end() && it->second.size() > 0) {
				auto &privileges = it->second;
				auto priv = privileges.find(privilege);
				if (priv != privileges.end() && priv->second->privileges >= 1 &&
				    priv->second->privileges & privilege_option)
					continue; // No Condition is required, If user is allowed
			}
			exp->alias = alias;
			if (add_or) {
				result = make_uniq<ConjunctionExpression>(conjuctiontype, std::move(result), std::move(exp));
				result->alias = alias;
			} else
				result = std::move(exp);
			add_or = true;
		}

		if (new_transaction)
			context.transaction.Commit();

		if (where_clause) {
			if (result)
				return make_uniq<ConjunctionExpression>(ExpressionType::CONJUNCTION_AND, std::move(result),
				                                        std::move(where_clause));
			else
				return std::move(where_clause);
		} else
			return result;
	}
	case TableReferenceType::JOIN: {
		auto &basetable = (JoinRef &)tableref;
		auto left = AddFortressExpression((TableRef &)*basetable.left, std::move(where_clause), privilege_option);
		return AddFortressExpression((TableRef &)*basetable.right, std::move(left), privilege_option);
	}
	default:
		return std::move(where_clause);
	}
}

unique_ptr<ParsedExpression> Authorizer::GetFortressExpression(string schema_name, string table_name,
                                                               duckdb_libpgquery::PGPrivilegeOption privilege_option) {
	unique_ptr<ParsedExpression> result;

	bool new_transaction = !context.transaction.HasActiveTransaction();
	if (new_transaction)
		context.transaction.BeginTransaction();

	auto table_entry = Catalog::GetEntry<TableCatalogEntry>(context, INVALID_CATALOG, schema_name, table_name,
	                                                        OnEntryNotFound::THROW_EXCEPTION);
	if (table_entry->fortress.size() == 0)
		return result;

	auto it = GetCurrentRole()->privileges.find(CatalogType::FORTRESS_ENTRY);
	bool add_or = false;
	for (auto privilege : table_entry->fortress) {
		auto fortress_entry = Catalog::GetEntry<FortressCatalogEntry>(context, INVALID_CATALOG, SECURITY_SCHEMA,
		                                                              privilege, OnEntryNotFound::RETURN_NULL);
		if (!fortress_entry || !fortress_entry->isLocked())
			continue;
		auto exp = fortress_entry->complement_expression->Copy();
		auto conjuctiontype = ExpressionType::CONJUNCTION_AND;
		if (it != GetCurrentRole()->privileges.end() && it->second.size() > 0) {
			auto &privileges = it->second;
			auto priv = privileges.find(privilege);
			if (priv != privileges.end() && priv->second->privileges >= 1 &&
			    priv->second->privileges & privilege_option)
				continue; // No Condition is required, If user is allowed to insert or update
		}
		if (add_or)
			result = make_uniq<ConjunctionExpression>(conjuctiontype, std::move(result), std::move(exp));
		else
			result = std::move(exp);
		add_or = true;
	}

	if (new_transaction)
		context.transaction.Commit();

	return result;
}

void Authorizer::BuildFortressConstraints(string schema_name, string table_name,
                                          duckdb_libpgquery::PGPrivilegeOption privilege_option) {
	schema_name = schema_name.empty() ? DEFAULT_SCHEMA : schema_name;
	string key = schema_name + "." + table_name;
	auto table_it = constrained_tables.find(key);
	if (table_it != constrained_tables.end())
		return;

	auto exp = GetFortressExpression(schema_name, table_name, privilege_option);
	if (exp) {
		bool new_transaction = !context.transaction.HasActiveTransaction();
		if (new_transaction)
			context.transaction.BeginTransaction();

		auto table_entry = Catalog::GetEntry<TableCatalogEntry>(context, INVALID_CATALOG, schema_name, table_name,
		                                                        OnEntryNotFound::THROW_EXCEPTION);
		table_entry->fortress_constraints.clear();
		if (table_entry->fortress.size() > 0) {
			auto binder = Binder::CreateBinder(context);
			auto bound_constraint = make_uniq<BoundCheckConstraint>();
			// check constraint: bind the expression
			CheckBinder check_binder(*binder, binder->context, table_entry->name, table_entry->GetColumns(),
			                         bound_constraint->bound_columns);
			bound_constraint->expression = check_binder.Bind(exp);
			table_entry->fortress_constraints.push_back(std::move(bound_constraint));
		}
		if (new_transaction)
			context.transaction.Commit();
	}
	constrained_tables[key] = schema_name + "." + table_name;
}

bool Authorizer::IsSuperuser() {
	if (GetCurrentRole()->superuser)
		return true;
	return false;
}

duckdb_libpgquery::PGPrivilegeOption Authorizer::GetPrivilege(StatementType type) {
	switch (type) {
	case StatementType::EXPORT_STATEMENT:
	case StatementType::SELECT_STATEMENT:
		return duckdb_libpgquery::PG_PRIVILEGE_SELECT;
	case StatementType::CREATE_STATEMENT:
		return duckdb_libpgquery::PG_PRIVILEGE_CREATE;
	case StatementType::DROP_STATEMENT:
		return duckdb_libpgquery::PG_PRIVILEGE_DROP;
	case StatementType::INSERT_STATEMENT:
		return duckdb_libpgquery::PG_PRIVILEGE_INSERT;
	case StatementType::COPY_STATEMENT:
		return duckdb_libpgquery::PG_PRIVILEGE_COPY;
	case StatementType::DELETE_STATEMENT:
		return duckdb_libpgquery::PG_PRIVILEGE_DELETE;
	case StatementType::UPDATE_STATEMENT:
		return duckdb_libpgquery::PG_PRIVILEGE_UPDATE;
	case StatementType::ALTER_STATEMENT:
		return duckdb_libpgquery::PG_PRIVILEGE_ALTER;
	case StatementType::EXECUTE_STATEMENT:
	case StatementType::CALL_STATEMENT:
		return duckdb_libpgquery::PG_PRIVILEGE_EXECUTE;
	case StatementType::VACUUM_STATEMENT:
		return duckdb_libpgquery::PG_PRIVILEGE_CREATE;
	case StatementType::LOAD_STATEMENT:
		return duckdb_libpgquery::PG_PRIVILEGE_LOAD;
	default:
		return duckdb_libpgquery::PG_PRIVILEGE_OPT;
	}
}

duckdb_libpgquery::PGPrivilegeOption Authorizer::GetPrivilege(duckdb_libpgquery::PGNodeTag type) {
	switch (type) {
	case duckdb_libpgquery::T_PGExportStmt:
	case duckdb_libpgquery::T_PGSelectStmt:
		return duckdb_libpgquery::PG_PRIVILEGE_SELECT;
	case duckdb_libpgquery::T_PGCreateStmt:
	case duckdb_libpgquery::T_PGCreateSchemaStmt:
	case duckdb_libpgquery::T_PGViewStmt:
	case duckdb_libpgquery::T_PGCreateSeqStmt:
	case duckdb_libpgquery::T_PGCreateFunctionStmt:
	case duckdb_libpgquery::T_PGCreateTableAsStmt:
	case duckdb_libpgquery::T_PGCreateRoleStmt:
	case duckdb_libpgquery::T_PGCreateTagStmt:
	case duckdb_libpgquery::T_PGCreateConfigStmt:
	case duckdb_libpgquery::T_PGCreateFortressStmt:
		return duckdb_libpgquery::PG_PRIVILEGE_CREATE;
	case duckdb_libpgquery::T_PGDropStmt:
		return duckdb_libpgquery::PG_PRIVILEGE_DROP;
	case duckdb_libpgquery::T_PGImportStmt:
	case duckdb_libpgquery::T_PGInsertStmt:
		return duckdb_libpgquery::PG_PRIVILEGE_INSERT;
	case duckdb_libpgquery::T_PGCopyStmt:
		return duckdb_libpgquery::PG_PRIVILEGE_COPY;
	case duckdb_libpgquery::T_PGDeleteStmt:
		return duckdb_libpgquery::PG_PRIVILEGE_DELETE;
	case duckdb_libpgquery::T_PGUpdateStmt:
		return duckdb_libpgquery::PG_PRIVILEGE_UPDATE;
	case duckdb_libpgquery::T_PGIndexStmt:
		return duckdb_libpgquery::PG_PRIVILEGE_CREATE;
	case duckdb_libpgquery::T_PGAlterTableStmt:
	case duckdb_libpgquery::T_PGRenameStmt:
	case duckdb_libpgquery::T_PGAlterSeqStmt:
	case duckdb_libpgquery::T_PGAlterRoleStmt:
		return duckdb_libpgquery::PG_PRIVILEGE_ALTER;
	case duckdb_libpgquery::T_PGExecuteStmt:
	case duckdb_libpgquery::T_PGCallStmt:
		return duckdb_libpgquery::PG_PRIVILEGE_EXECUTE;
	case duckdb_libpgquery::T_PGVacuumStmt:
		return duckdb_libpgquery::PG_PRIVILEGE_ALL;
	case duckdb_libpgquery::T_PGLoadStmt:
		return duckdb_libpgquery::PG_PRIVILEGE_LOAD;
		return duckdb_libpgquery::PG_PRIVILEGE_ALL;
	case duckdb_libpgquery::T_PGGrantStmt:
	case duckdb_libpgquery::T_PGRevokeStmt:
		return duckdb_libpgquery::PG_PRIVILEGE_CREATE;
	default:
		return duckdb_libpgquery::PG_PRIVILEGE_OPT;
	}
}

void Authorizer::Authorize(CatalogType catalog_type, string catalog_name,
                           duckdb_libpgquery::PGPrivilegeOption privilege_option, bool checkgrantoption) {

	if (GetCurrentRole()->superuser)
		return;

	auto &all_privileges = GetCurrentRole()->privileges[catalog_type];
	if (!all_privileges.empty()) {
		auto privilege = all_privileges[catalog_name].get();
		if (privilege) {
			if ((privilege->privileges & privilege_option) ||
			    (privilege->privileges & duckdb_libpgquery::PG_PRIVILEGE_ALL)) {
				if (!checkgrantoption || privilege->grantOption)
					return;
			} else
				throw PermissionException("Access Denied.");
		}
	}

	throw PermissionException("Access Denied.");
}

vector<string> Authorizer::GetUnauthorizedColumns(string schema_name, string table_name) {
	vector<string> result;

	if (GetCurrentRole()->superuser)
		return result;

	auto &all_privileges = GetCurrentRole()->privileges[CatalogType::TABLE_ENTRY];
	if (!all_privileges.empty()) {
		auto privilege = all_privileges[table_name].get();
		if (privilege)
			result = privilege->unauthorized_columns;
	}

	return result;
}

vector<string> Authorizer::GetUnauthorizedColumns(BaseTableRef &basetableref) {
	return GetUnauthorizedColumns(basetableref.schema_name, basetableref.table_name);
}

void Authorizer::Authorize_table(string schema_name, string table_name,
                                 duckdb_libpgquery::PGPrivilegeOption privilege_option, bool checkgrantoption) {
	if (GetCurrentRole()->superuser)
		return;

	try {
		Authorize(CatalogType::TABLE_ENTRY, table_name, privilege_option, checkgrantoption);
	} catch (const PermissionException &e) {
		Authorize_schema(schema_name, privilege_option, checkgrantoption);
	}

	if (privilege_option == duckdb_libpgquery::PG_PRIVILEGE_INSERT ||
	    privilege_option == duckdb_libpgquery::PG_PRIVILEGE_UPDATE)
		BuildFortressConstraints(schema_name, table_name, privilege_option);
}

void Authorizer::Authorize_table(string schema_name, string table_name, StatementType statement_type) {
	auto privilege_option = GetPrivilege(statement_type);
	Authorize_table(schema_name, table_name, privilege_option);
}

void Authorizer::Authorize_table(string schema_name, string table_name, duckdb_libpgquery::PGNodeTag statement_type,
                                 bool checkgrantoption) {
	auto privilege_option = GetPrivilege(statement_type);
	Authorize_table(schema_name, table_name, privilege_option, checkgrantoption);
}

void Authorizer::Authorize_view(string schema_name, string view_name, StatementType statement_type) {
	auto privilege_option = GetPrivilege(statement_type);
	try {
		Authorize(CatalogType::VIEW_ENTRY, view_name, privilege_option);
	} catch (const PermissionException &e) {
		Authorize_schema(schema_name, privilege_option);
	}
}

void Authorizer::Authorize_view(string schema_name, string view_name,
                                duckdb_libpgquery::PGPrivilegeOption privilege_option, bool checkgrantoption) {
	try {
		Authorize(CatalogType::VIEW_ENTRY, view_name, privilege_option, checkgrantoption);
	} catch (const PermissionException &e) {
		Authorize_schema(schema_name, privilege_option, checkgrantoption);
	}
}

void Authorizer::Authorize_table(BaseTableRef &tableref, duckdb_libpgquery::PGPrivilegeOption privilege_option,
                                 bool checkgrantoption) {
	if (GetCurrentRole()->superuser)
		return;
	Authorize_table(tableref.schema_name, tableref.table_name, privilege_option, checkgrantoption);
}

void Authorizer::Authorize_table(TableRef &tableref, duckdb_libpgquery::PGNodeTag statement_type,
                                 bool checkgrantoption) {
	if (GetCurrentRole()->superuser)
		return;
	auto privilege_option = GetPrivilege(statement_type);

	Authorize_table(tableref, privilege_option, checkgrantoption);
}

void Authorizer::Authorize_Columns(TableRef &tableref, StarExpression &starexpression) {
	if (GetCurrentRole()->superuser)
		return;

	switch (tableref.type) {
	case TableReferenceType::BASE_TABLE: {
		auto &basetable = (BaseTableRef &)tableref;
		auto unauthorized_columns = GetUnauthorizedColumns(basetable);
		for (auto &column_name : unauthorized_columns) {
			if (starexpression.exclude_list.find(column_name) == starexpression.exclude_list.end())
				starexpression.exclude_list.insert(std::move(column_name));
		}
		break;
	}
	case TableReferenceType::JOIN: {
		auto &basetable = (JoinRef &)tableref;
		Authorize_Columns((TableRef &)*basetable.left, starexpression);
		Authorize_Columns((TableRef &)*basetable.right, starexpression);
		break;
	}
	default:
		return;
	}
}

void Authorizer::Authorize_Columns(TableRef &tableref, vector<string> select_list) {
	if (GetCurrentRole()->superuser)
		return;

	switch (tableref.type) {
	case TableReferenceType::BASE_TABLE: {
		bool new_transaction = !context.transaction.HasActiveTransaction();
		if (new_transaction)
			context.transaction.BeginTransaction();

		auto &basetable = (BaseTableRef &)tableref;
		auto unauthorized_columns = GetUnauthorizedColumns(basetable);
		auto table_entry = Catalog::GetEntry<TableCatalogEntry>(context, INVALID_CATALOG, basetable.schema_name,
		                                                        basetable.table_name, OnEntryNotFound::RETURN_NULL);
		if (new_transaction)
			context.transaction.Commit();
		auto &all_privileges = GetCurrentRole()->privileges[CatalogType::TAG_ENTRY];
		for (idx_t i = 0; i < select_list.size(); i++) {
			if (std::find(unauthorized_columns.begin(), unauthorized_columns.end(), select_list[i]) !=
			    unauthorized_columns.end())
				throw PermissionException("Access Denied on column %s !", select_list[i]);

			if (table_entry) {
				auto &col = table_entry->GetColumn(select_list[i]);
				for (auto tag_name : col.tag_names) {
					if (!all_privileges.empty()) {
						auto privilege = all_privileges[tag_name].get();
						if (!privilege)
							throw PermissionException("Access Denied to tag %s", tag_name);
					} else
						throw PermissionException("Access Denied to tag %s", tag_name);
				}
			}
		}
		break;
	}
	case TableReferenceType::JOIN: {
		auto &basetable = (JoinRef &)tableref;
		Authorize_Columns((TableRef &)*basetable.left, select_list);
		Authorize_Columns((TableRef &)*basetable.right, select_list);
		break;
	}
	default:
		return;
	}
}

void Authorizer::Authorize_Tag(string schema_name, string tag_name) {
	if (GetCurrentRole()->superuser)
		return;

	auto &all_privileges = GetCurrentRole()->privileges[CatalogType::TAG_ENTRY];
	if (!all_privileges.empty()) {
		auto privilege = all_privileges[tag_name].get();
		if (!privilege)
			throw PermissionException("Access Denied to tag %s", tag_name);
		return;
	}
	throw PermissionException("Access Denied to tag %s", tag_name);
}

void Authorizer::Authorize_Column(string schema_name, string table_name, string column_name) {
	if (GetCurrentRole()->superuser)
		return;

	auto &all_privileges = GetCurrentRole()->privileges[CatalogType::TABLE_ENTRY];
	if (!all_privileges.empty()) {
		auto privilege = all_privileges[table_name].get();
		if (privilege && std::find(privilege->unauthorized_columns.begin(), privilege->unauthorized_columns.end(),
		                           column_name) != privilege->unauthorized_columns.end())
			throw PermissionException("Access Denied to column %s", column_name);
	}

	bool new_transaction = !context.transaction.HasActiveTransaction();
	if (new_transaction)
		context.transaction.BeginTransaction();
	auto table_entry = Catalog::GetEntry<TableCatalogEntry>(context, INVALID_CATALOG, schema_name, table_name,
	                                                        OnEntryNotFound::RETURN_NULL);
	if (new_transaction)
		context.transaction.Commit();
	if (table_entry) {
		auto &all_privileges = GetCurrentRole()->privileges[CatalogType::TAG_ENTRY];
		auto &col = table_entry->GetColumn(column_name);
		for (auto tag_name : col.tag_names) {
			if (!all_privileges.empty()) {
				auto privilege = all_privileges[tag_name].get();
				if (!privilege)
					throw PermissionException("Access Denied to tag %s", tag_name);
				else if (!(privilege->privileges & duckdb_libpgquery::PG_PRIVILEGE_SELECT))
					throw PermissionException("Role Does not have SELECT Access on tag %s", tag_name);
			} else
				throw PermissionException("Access Denied to tag %s", tag_name);
		}
	}
}

void Authorizer::Authorize_table(TableRef &tableref, duckdb_libpgquery::PGPrivilegeOption privilege_option,
                                 bool checkgrantoption) {
	if (GetCurrentRole()->superuser)
		return;

	switch (tableref.type) {
	case TableReferenceType::BASE_TABLE: {
		auto &basetable = (BaseTableRef &)tableref;
		Authorize_table(basetable.schema_name, basetable.table_name, privilege_option, checkgrantoption);
		break;
	}
	case TableReferenceType::JOIN: {
		auto &basetable = (JoinRef &)tableref;
		Authorize_table((TableRef &)*basetable.left, privilege_option, checkgrantoption);
		Authorize_table((TableRef &)*basetable.right, privilege_option, checkgrantoption);
		break;
	}
	default:
		return;
	}
}

void Authorizer::Authorize_schema(string schema_name, duckdb_libpgquery::PGPrivilegeOption privilege_option,
                                  bool checkgrantoption) {
	if (GetCurrentRole()->superuser)
		return;

	schema_name = schema_name.empty() ? DEFAULT_SCHEMA : schema_name;
	Authorize(CatalogType::SCHEMA_ENTRY, schema_name, privilege_option, checkgrantoption);
}

void Authorizer::AuthorizeWhereClauseColumn(duckdb_libpgquery::PGColumnRef *root,
                                            const vector<string> &unauthorized_columns) {
	if (!root) {
		return;
	}

	if (root->type != duckdb_libpgquery::T_PGColumnRef) {
		return;
	}

	auto fields = root->fields;
	auto head_node = (duckdb_libpgquery::PGNode *)fields->head->data.ptr_value;
	switch (head_node->type) {
	case duckdb_libpgquery::T_PGString: {
		if (fields->length < 1) {
			return;
		}
		if (fields->length == 1) {
			auto column_name =
			    string(reinterpret_cast<duckdb_libpgquery::PGValue *>(fields->head->data.ptr_value)->val.str);
			if (std::find(unauthorized_columns.begin(), unauthorized_columns.end(), column_name) !=
			    unauthorized_columns.end())
				throw PermissionException("Access Denied to column %s", column_name);
		} else if (fields->length == 2) {
			auto col_node = reinterpret_cast<duckdb_libpgquery::PGNode *>(fields->head->next->data.ptr_value);
			switch (col_node->type) {
			case duckdb_libpgquery::T_PGString: {
				auto column_name = string(reinterpret_cast<duckdb_libpgquery::PGValue *>(col_node)->val.str);
				if (std::find(unauthorized_columns.begin(), unauthorized_columns.end(), column_name) !=
				    unauthorized_columns.end()) {
					throw PermissionException("Access Denied to column %s", column_name);
				}
				return;
			}
			default:
				return;
			}
		} else
			return;
	}
	default:
		return;
	}
}

void Authorizer::AuthorizeWhereClause(duckdb_libpgquery::PGNode *node, const vector<string> &unauthorized_columns) {
	if (!node) {
		return;
	}

	switch (node->type) {
	case duckdb_libpgquery::T_PGBoolExpr: {
		auto root_boolexpr = reinterpret_cast<duckdb_libpgquery::PGBoolExpr *>(node);
		if (root_boolexpr) {
			for (auto child_node = root_boolexpr->args->head; child_node != nullptr; child_node = child_node->next)
				AuthorizeWhereClause(reinterpret_cast<duckdb_libpgquery::PGNode *>(child_node->data.ptr_value),
				                     unauthorized_columns);
		}
		return;
	}
	case duckdb_libpgquery::T_PGAExpr: {
		auto root_aexpr = reinterpret_cast<duckdb_libpgquery::PGAExpr *>(node);
		if (root_aexpr) {
			AuthorizeWhereClauseColumn(reinterpret_cast<duckdb_libpgquery::PGColumnRef *>(root_aexpr->lexpr),
			                           unauthorized_columns);
			AuthorizeWhereClauseColumn(reinterpret_cast<duckdb_libpgquery::PGColumnRef *>(root_aexpr->rexpr),
			                           unauthorized_columns);
		}
		return;
	}
	default:
		return;
	}
}

} // namespace duckdb
