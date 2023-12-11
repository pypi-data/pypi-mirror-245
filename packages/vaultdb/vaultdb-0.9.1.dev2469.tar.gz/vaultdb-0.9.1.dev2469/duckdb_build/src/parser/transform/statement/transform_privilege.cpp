#include "duckdb/parser/parsed_data/create_role_info.hpp"
#include "duckdb/parser/statement/alter_statement.hpp"
#include "duckdb/parser/statement/create_statement.hpp"
#include "duckdb/parser/transformer.hpp"

namespace duckdb {

unique_ptr<AlterStatement> Transformer::TransformPrivilege(AlterRoleType type, duckdb_libpgquery::PGGrantStmt &stmt) {
	auto result = make_uniq<AlterStatement>();
	bool modifygrantOption = false;
	if (stmt.grantoption & duckdb_libpgquery::PG_GRANTOPT_GRANT)
		modifygrantOption = true;

	auto catalogType = CatalogType::TABLE_ENTRY;

	switch (stmt.resourcetype) {
	case duckdb_libpgquery::PG_OBJECT_TABLE:
		catalogType = CatalogType::TABLE_ENTRY;
		if (!stmt.resourcename->relname)
			throw InvalidInputException("Table Name is Required");
		// Authorize role
		if (context)
			context->authorizer->Authorize_table(
			    DEFAULT_SCHEMA, stmt.resourcename->relname,
			    static_cast<duckdb_libpgquery::PGPrivilegeOption>(stmt.privilegeOptions), true);
		break;
	case duckdb_libpgquery::PG_OBJECT_SCHEMA:
		catalogType = CatalogType::SCHEMA_ENTRY;
		// Authorize role
		if (!stmt.resourcename->relname)
			throw InvalidInputException("Schema Name is Required");
		if (context)
			context->authorizer->Authorize_schema(
			    stmt.resourcename->relname, static_cast<duckdb_libpgquery::PGPrivilegeOption>(stmt.privilegeOptions),
			    true);
		break;
	case duckdb_libpgquery::PG_OBJECT_VIEW:
		catalogType = CatalogType::VIEW_ENTRY;
		if (!stmt.resourcename->relname)
			throw InvalidInputException("View Name is Required");
		// Authorize role
		if (context)
			context->authorizer->Authorize_view(DEFAULT_SCHEMA, stmt.resourcename->relname,
			                                   static_cast<duckdb_libpgquery::PGPrivilegeOption>(stmt.privilegeOptions),
			                                   true);

		break;
	case duckdb_libpgquery::PG_OBJECT_TAG:
		catalogType = CatalogType::TAG_ENTRY;
		if (!stmt.resourcename->relname)
			throw InvalidInputException("TAG Name is Required");
		// Authorize role
		if (context)
			context->authorizer->Authorize_schema(
			    DEFAULT_SCHEMA, static_cast<duckdb_libpgquery::PGPrivilegeOption>(stmt.privilegeOptions), true);

		break;
	case duckdb_libpgquery::PG_OBJECT_CONFIG:
		catalogType = CatalogType::CONFIG_ENTRY;
		if (!stmt.resourcename->relname)
			throw InvalidInputException("CONFIG Name is Required");
		// Authorize role
		if (context)
			context->authorizer->Authorize_schema(
			    DEFAULT_SCHEMA, static_cast<duckdb_libpgquery::PGPrivilegeOption>(stmt.privilegeOptions), true);

		break;
	case duckdb_libpgquery::PG_OBJECT_FORTRESS:
		catalogType = CatalogType::FORTRESS_ENTRY;
		if (!stmt.resourcename->relname)
			throw InvalidInputException("FORTRESS Name is Required");
		// Authorize role
		if (context)
			context->authorizer->Authorize_schema(
			    DEFAULT_SCHEMA, static_cast<duckdb_libpgquery::PGPrivilegeOption>(stmt.privilegeOptions), true);

		break;
	default:
		throw NotImplementedException("Cannot apply privileges to this type yet");
	}

	AlterEntryData data(INVALID_CATALOG, SECURITY_SCHEMA, stmt.role->relname, OnEntryNotFound::RETURN_NULL);
	auto info = make_uniq<ModifyRolePrivilegeInfo>(type, std::move(data), catalogType, stmt.resourcename->relname,
	                                               stmt.privilegeOptions, modifygrantOption);

	if (catalogType == CatalogType::TABLE_ENTRY && stmt.aliases &&
	    (stmt.privilegeOptions & duckdb_libpgquery::PG_PRIVILEGE_SELECT)) {

		if (type == AlterRoleType::REVOKE_PRIVILEGES)
			info->privileges &= ~duckdb_libpgquery::PG_PRIVILEGE_SELECT;

		for (auto c = stmt.aliases->head; c != nullptr; c = lnext(c)) {
			auto node = reinterpret_cast<duckdb_libpgquery::PGNode *>(c->data.ptr_value);
			switch (node->type) {
			case duckdb_libpgquery::T_PGString: {
				auto val = (duckdb_libpgquery::PGValue *)node;
				info->aliases.emplace_back(val->val.str);
				break;
			}
			default:
				throw NotImplementedException("Role Column type");
			}
		}
	} else if (stmt.aliases && !(stmt.privilegeOptions & duckdb_libpgquery::PG_PRIVILEGE_SELECT)) {
		throw NotImplementedException("List of columns are only supported for SELECT on TABLE/TAG");
	}

	result->info = std::move(info);
	return result;
}

} // namespace duckdb
