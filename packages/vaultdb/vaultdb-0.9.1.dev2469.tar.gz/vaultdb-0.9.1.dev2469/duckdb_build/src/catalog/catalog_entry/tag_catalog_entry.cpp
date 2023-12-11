#include "duckdb/catalog/catalog_entry/tag_catalog_entry.hpp"

#include "duckdb/catalog/catalog_entry/schema_catalog_entry.hpp"
#include "duckdb/catalog/dependency_manager.hpp"
#include "duckdb/common/exception.hpp"

#include <algorithm>
#include <sstream>

namespace duckdb {

TagCatalogEntry::TagCatalogEntry(Catalog &catalog, SchemaCatalogEntry &schema, CreateTagInfo &info)
    : StandardEntry(CatalogType::TAG_ENTRY, schema, catalog, info.name), comment(std::move(info.comment)),
      function(std::move(info.function)) {
}

unique_ptr<CatalogEntry> TagCatalogEntry::AlterEntry(ClientContext &context, AlterInfo &alterinfo) {
	throw InternalException("Tag Alter is not supported yet! Please drop and recreate");
}

unique_ptr<CreateInfo> TagCatalogEntry::GetInfo() const {
	auto result = make_uniq<CreateTagInfo>();
	result->schema = schema.name;
	result->name = name;
	result->name = comment;
	result->function = function->Copy();
	return std::move(result);
}

string TagCatalogEntry::ToSQL() const {
	std::stringstream ss;
	ss << "CREATE TAG ";
	ss << name;
	ss << " AS '";
	ss << comment;
	ss << "';";
	return ss.str();
}

} // namespace duckdb
