//===----------------------------------------------------------------------===//
//                         DuckDB
//
// duckdb/parser/parsed_data/create_table_info.hpp
//
//
//===----------------------------------------------------------------------===//

#pragma once

#include "duckdb/common/common.hpp"
#include "duckdb/parser/expression/constant_expression.hpp"
#include "duckdb/parser/expression/function_expression.hpp"
#include "duckdb/parser/parsed_data/create_info.hpp"
#include "duckdb/common/set.hpp"
#include "duckdb/common/unordered_set.hpp"
#include "duckdb/parser/column_definition.hpp"
#include "duckdb/parser/constraint.hpp"
#include "duckdb/parser/tableref/basetableref.hpp"
#include "duckdb/parser/statement/select_statement.hpp"
#include "duckdb/parser/query_node/select_node.hpp"
#include "duckdb/main/relation/value_relation.hpp"
#include "duckdb/parser/statement/insert_statement.hpp"
#include "duckdb/catalog/catalog_entry/column_dependency_manager.hpp"
#include "duckdb/parser/column_list.hpp"

#include <algorithm>

namespace duckdb {
class SchemaCatalogEntry;

struct CreateTableInfo : public CreateInfo {
	DUCKDB_API CreateTableInfo();
	DUCKDB_API CreateTableInfo(string catalog, string schema, string name);
	DUCKDB_API CreateTableInfo(SchemaCatalogEntry &schema, string name);

	//! Table name to insert to
	string table;
	//! List of columns of the table
	ColumnList columns;
	//! List of constraints on the table
	vector<unique_ptr<Constraint>> constraints;
	//! List of partition by columns on the table
	vector<string> partition_key_columns;
	//! CREATE TABLE as QUERY
	unique_ptr<SelectStatement> query;
	//! Attached Fortress names
	unordered_set<string> fortress;
public:
	DUCKDB_API unique_ptr<CreateInfo> Copy() const override;

	DUCKDB_API void Serialize(Serializer &serializer) const override;
	DUCKDB_API static unique_ptr<CreateInfo> Deserialize(Deserializer &deserializer);

	string ToString() const override;
};

} // namespace duckdb
