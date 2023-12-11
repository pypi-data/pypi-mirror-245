//===----------------------------------------------------------------------===//
//                         DuckDB
//
// duckdb/parser/parsed_data/Push_table_data.hpp
//
//
//===----------------------------------------------------------------------===//

#pragma once

#include "duckdb/parser/parsed_data/parse_info.hpp"
#include "duckdb/common/types/value.hpp"

namespace duckdb {
class TableCatalogEntry;

struct PushedTableData {
	//! Name of the Pushed table
	string table_name;

	//! Name of the schema
	string schema_name;

	//! Name of the database
	string database_name;

	//! Path to be Pushed
	string file_path;
};

struct PushedTableInfo {
	TableCatalogEntry *entry;
	PushedTableData table_data;
};

struct BoundPushData : public ParseInfo {
	std::vector<PushedTableInfo> data;
};

} // namespace duckdb
