//===----------------------------------------------------------------------===//
//                         DuckDB
//
// duckdb/catalog/catalog_entry/config_catalog_entry.hpp
//
//
//===----------------------------------------------------------------------===//

#pragma once

#include "duckdb/catalog/standard_entry.hpp"
#include "duckdb/common/mutex.hpp"
#include "duckdb/parser/parsed_data/create_config_info.hpp"

namespace duckdb {
class Serializer;
class Deserializer;

//! A Config catalog entry
class ConfigCatalogEntry : public StandardEntry {
public:
	static constexpr const CatalogType Type = CatalogType::CONFIG_ENTRY;
	static constexpr const char *Name = "config";

public:
	//! Create a real Config and initialize storage for it
	ConfigCatalogEntry(Catalog &catalog, SchemaCatalogEntry &schema, CreateConfigInfo &info);

	//! config value
	string value = string();

public:
	unique_ptr<CreateInfo> GetInfo() const override;

	DUCKDB_API string ToSQL() const override;
};
} // namespace duckdb
