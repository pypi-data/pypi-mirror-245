//===----------------------------------------------------------------------===//
//                         DuckDB
//
// duckdb/main/authorizer.hpp
//
//
//===----------------------------------------------------------------------===//

#pragma once

#include "duckdb/common/map.hpp"
#include "duckdb/catalog/catalog_entry/schema_catalog_entry.hpp"
#include "duckdb/catalog/catalog_set.hpp"
#include "duckdb/parser/tokens.hpp"
#include "duckdb/parser/tableref/basetableref.hpp"
#include "duckdb/parser/sql_statement.hpp"

#include "pg_definitions.hpp"
#include "nodes/parsenodes.hpp"

namespace duckdb {
class ClientContext;
class DatabaseInstance;
struct CreateRoleInfo;
class StarExpression;
class ParsedExpression;

//! The Authorizer class is responsible for Authorization
class Authorizer : public std::enable_shared_from_this<Authorizer> {

public:
	explicit Authorizer(ClientContext &context, string role);

	ClientContext &context;

private:
	string role;
	//! The current role used in client context
	shared_ptr<CreateRoleInfo> current_role;

	//Tables constrained for the role
	map<string, string> constrained_tables;

public:
	//! Connect using role
	void Role(const string &role);

	//! Returns the current role info (if any)
	shared_ptr<CreateRoleInfo> GetCurrentRole();
	
	unique_ptr<ParsedExpression> AddFortressExpression(TableRef &tableref, unique_ptr<ParsedExpression> where_clause, duckdb_libpgquery::PGPrivilegeOption privilege_option);

	unique_ptr<ParsedExpression> GetFortressExpression(string schema_name, string table_name, duckdb_libpgquery::PGPrivilegeOption privilege_option);

	void BuildFortressConstraints(string schema_name, string table_name, duckdb_libpgquery::PGPrivilegeOption privilege_option);

	duckdb_libpgquery::PGPrivilegeOption GetPrivilege(StatementType type);
	
	duckdb_libpgquery::PGPrivilegeOption GetPrivilege(duckdb_libpgquery::PGNodeTag type);

	bool IsGrantRevokeAllowed();

	bool IsSuperuser();
	
	vector<string> GetUnauthorizedColumns(string schema_name, string table_name);

	vector<string> GetUnauthorizedColumns(BaseTableRef &tableref);

	void Authorize(CatalogType catalog_type, string catalog_name, duckdb_libpgquery::PGPrivilegeOption privilege_option, bool checkgrantoption=false);

	void Authorize_Columns(TableRef &tableref, StarExpression &starexpression);

	void Authorize_Columns(TableRef &tableref, vector<string> select_list);
	
	void Authorize_Column(string schema_name, string table_name, string column_name);
	
	void Authorize_Tag(string schema_name, string tag_name);

	//void Authorize_table(TableRef &tableref, StatementType statement_type, bool checkgrantoption=false);
	void Authorize_table(TableRef &tableref, duckdb_libpgquery::PGNodeTag statement_type, bool checkgrantoption=false);
	void Authorize_table(TableRef &tableref, duckdb_libpgquery::PGPrivilegeOption privilege_option, bool checkgrantoption=false);
	
	void Authorize_table(BaseTableRef &tableref, duckdb_libpgquery::PGPrivilegeOption privilege_option, bool checkgrantoption=false);
	
	void Authorize_table(string schema_name, string table_name, StatementType statement_type);
	void Authorize_table(string schema_name, string table_name, duckdb_libpgquery::PGNodeTag statement_type, bool checkgrantoption=false);
	void Authorize_table(string schema_name, string table_name, duckdb_libpgquery::PGPrivilegeOption privilege_option, bool checkgrantoption=false);
	
	void Authorize_view(string schema_name, string view_name, StatementType statement_type);
	void Authorize_view(string schema_name, string view_name, duckdb_libpgquery::PGPrivilegeOption privilege_option, bool checkgrantoption=false);
	
	void Authorize_schema(string schema_name, duckdb_libpgquery::PGPrivilegeOption privilege_option, bool checkgrantoption=false);
	
	void AuthorizeWhereClause(duckdb_libpgquery::PGNode *node, const vector<string> &unauthorized_columns);
	void AuthorizeWhereClauseColumn(duckdb_libpgquery::PGColumnRef *root, const vector<string> &unauthorized_columns);
}; 

} // namespace duckdb
