//===----------------------------------------------------------------------===//
//                         DuckDB
//
// duckdb/catalog/catalog_entry/sequence_catalog_entry.hpp
//
//
//===----------------------------------------------------------------------===//

#pragma once

#include "duckdb/catalog/standard_entry.hpp"
#include "duckdb/common/mutex.hpp"
#include "duckdb/parser/parsed_data/create_fortress_info.hpp"

namespace duckdb {
class Serializer;
class Deserializer;
struct AlterInfo;

//! A Fortress catalog entry
class FortressCatalogEntry : public StandardEntry {
public:
	static constexpr const CatalogType Type = CatalogType::FORTRESS_ENTRY;
	static constexpr const char *Name = "fortress";

public:
	//! Create a real FortressCatalogEntry and initialize storage for it
	FortressCatalogEntry(Catalog &catalog, SchemaCatalogEntry &schema, CreateFortressInfo &info);

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
	unique_ptr<CatalogEntry> AlterEntry(ClientContext &context, AlterInfo &info) override;
	bool isLocked();
	
	void AddFortressToTableEntry(ClientContext &context);

	unique_ptr<CreateInfo> GetInfo() const override;
	string ToSQL() const override;
};
} // namespace duckdb
