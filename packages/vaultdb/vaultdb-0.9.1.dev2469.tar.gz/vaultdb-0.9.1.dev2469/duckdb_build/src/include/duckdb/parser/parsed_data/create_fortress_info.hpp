//===----------------------------------------------------------------------===//
//                         DuckDB
//
// duckdb/parser/parsed_data/create_fortress_info.hpp
//
//
//===----------------------------------------------------------------------===//

#pragma once

#include "duckdb/common/limits.hpp"
#include "duckdb/common/map.hpp"
#include "duckdb/parser/parsed_data/create_info.hpp"
#include "duckdb/parser/tableref.hpp"
#include "duckdb/parser/parsed_expression.hpp"
#include "duckdb/parser/parsed_data/create_view_info.hpp"

namespace duckdb {

struct CreateFortressInfo : public CreateInfo {
	DUCKDB_API CreateFortressInfo() : CreateInfo(CatalogType::FORTRESS_ENTRY, SECURITY_SCHEMA), 
		name(string()), locked(false), start_date(string()), end_date(string()), unlocked_for_role(string()) {
	}

	//! fortress name to create
	string name;
	//! fortress lock info
	bool locked;
	string start_date;
	string end_date;
	string unlocked_for_role;
	//! The table to create the fortress on
	unique_ptr<TableRef> table;
	//! where clause
	unique_ptr<ParsedExpression> expression;
	unique_ptr<ParsedExpression> complement_expression;

public:
	DUCKDB_API unique_ptr<CreateInfo> Copy() const override;

	DUCKDB_API void Serialize(Serializer &serializer) const override;
	DUCKDB_API static unique_ptr<CreateInfo> Deserialize(Deserializer &deserializer);
};

} // namespace duckdb
