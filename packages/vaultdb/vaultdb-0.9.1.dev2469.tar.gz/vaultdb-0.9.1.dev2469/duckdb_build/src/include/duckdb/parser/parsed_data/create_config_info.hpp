//===----------------------------------------------------------------------===//
//                         DuckDB
//
// duckdb/parser/parsed_data/create_config_info.hpp
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

struct CreateConfigInfo : public CreateInfo {
	CreateConfigInfo() : CreateInfo(CatalogType::CONFIG_ENTRY, SECURITY_SCHEMA), 
		name(string()), value(string()) {
	}

	//! config name to create
	string name;
	//! External Data files Path
	string value;

public:
	unique_ptr<CreateInfo> Copy() const override;

	DUCKDB_API void Serialize(Serializer &serializer) const override;
	DUCKDB_API static unique_ptr<CreateInfo> Deserialize(Deserializer &deserializer);
};

} // namespace duckdb
