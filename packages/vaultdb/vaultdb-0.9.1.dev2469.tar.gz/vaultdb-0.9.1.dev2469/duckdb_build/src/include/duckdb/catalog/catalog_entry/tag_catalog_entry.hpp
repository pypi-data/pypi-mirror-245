//===----------------------------------------------------------------------===//
//                         DuckDB
//
// duckdb/catalog/catalog_entry/tag_catalog_entry.hpp
//
//
//===----------------------------------------------------------------------===//

#pragma once

#include "duckdb/catalog/standard_entry.hpp"
#include "duckdb/common/mutex.hpp"
#include "duckdb/parser/parsed_data/alter_table_info.hpp"
#include "duckdb/parser/parsed_data/create_tag_info.hpp"

namespace duckdb {
class Serializer;
class Deserializer;

//! A role catalog entry
class TagCatalogEntry : public StandardEntry {
public:
	static constexpr const CatalogType Type = CatalogType::TAG_ENTRY;
	static constexpr const char *Name = "tag";

public:
	//! Create a real TagCatalogEntry and initialize storage for it
	TagCatalogEntry(Catalog &catalog, SchemaCatalogEntry &schema, CreateTagInfo &info);

	//! tag comment to create
	string comment;
	//! tag function expression
	unique_ptr<ParsedExpression> function;

public:
	unique_ptr<CatalogEntry> AlterEntry(ClientContext &context, AlterInfo &info) override;

	unique_ptr<CreateInfo> GetInfo() const override;

	DUCKDB_API string ToSQL() const override;
};
} // namespace duckdb
