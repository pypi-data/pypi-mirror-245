//===----------------------------------------------------------------------===//
//                         DuckDB
//
// duckdb/parser/parsed_data/create_tag_info.hpp
//
//
//===----------------------------------------------------------------------===//

#pragma once

#include "duckdb/common/limits.hpp"
#include "duckdb/common/map.hpp"
#include "duckdb/common/unique_ptr.hpp"
#include "duckdb/parser/parsed_data/create_info.hpp"
#include "duckdb/parser/parsed_expression.hpp"

namespace duckdb {

struct CreateTagInfo : public CreateInfo {
	CreateTagInfo() : CreateInfo(CatalogType::TAG_ENTRY, SECURITY_SCHEMA), 
		name(string()), comment(string()) {
	}

	//! tag name to create
	string name;
	//! tag comment to create
	string comment;
	//! tag function expression
	unique_ptr<ParsedExpression> function;

public:
	unique_ptr<CreateInfo> Copy() const override;

	DUCKDB_API void Serialize(Serializer &serializer) const override;
	DUCKDB_API static unique_ptr<CreateInfo> Deserialize(Deserializer &deserializer);
};

} // namespace duckdb
