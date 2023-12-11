#include "duckdb/catalog/catalog_entry/config_catalog_entry.hpp"

#include "duckdb/catalog/catalog_entry/schema_catalog_entry.hpp"
#include "duckdb/catalog/dependency_manager.hpp"
#include "duckdb/common/exception.hpp"

#include <algorithm>
#include <sstream>

namespace duckdb {

ConfigCatalogEntry::ConfigCatalogEntry(Catalog &catalog, SchemaCatalogEntry &schema, CreateConfigInfo &info)
    : StandardEntry(CatalogType::CONFIG_ENTRY, schema, catalog, info.name), value(info.value) {
}

unique_ptr<CreateInfo> ConfigCatalogEntry::GetInfo() const {
	auto result = make_uniq<CreateConfigInfo>();
	result->schema = schema.name;
	result->name = name;
	result->value = value;
	return std::move(result);
}

string ConfigCatalogEntry::ToSQL() const {
	std::stringstream ss;
	ss << "CREATE CONFIG ";
	ss << name;
	ss << " ";
	ss << value;
	ss << "';";
	return ss.str();
}

} // namespace duckdb
