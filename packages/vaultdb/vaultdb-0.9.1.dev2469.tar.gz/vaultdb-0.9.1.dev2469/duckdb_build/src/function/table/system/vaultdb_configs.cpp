#include "duckdb/catalog/catalog.hpp"
#include "duckdb/catalog/catalog_entry/schema_catalog_entry.hpp"
#include "duckdb/catalog/catalog_entry/config_catalog_entry.hpp"
#include "duckdb/common/exception.hpp"
#include "duckdb/function/table/system_functions.hpp"
#include "duckdb/main/client_context.hpp"
#include "duckdb/main/client_data.hpp"
#include "duckdb/parser/constraint.hpp"
#include "duckdb/parser/constraints/unique_constraint.hpp"
#include "duckdb/storage/data_table.hpp"
#include "duckdb/storage/table_storage_info.hpp"

namespace duckdb {

struct VaultDBConfigsData : public GlobalTableFunctionState {
	VaultDBConfigsData() : offset(0) {
	}

	vector<reference<CatalogEntry>> entries;
	idx_t offset;
};

static unique_ptr<FunctionData> VaultDBConfigsBind(ClientContext &context, TableFunctionBindInput &input,
                                                 vector<LogicalType> &return_types, vector<string> &names) {
	names.emplace_back("database_name");
	return_types.emplace_back(LogicalType::VARCHAR);

	names.emplace_back("database_oid");
	return_types.emplace_back(LogicalType::BIGINT);

	names.emplace_back("schema_name");
	return_types.emplace_back(LogicalType::VARCHAR);

	names.emplace_back("schema_oid");
	return_types.emplace_back(LogicalType::BIGINT);

	names.emplace_back("config_name");
	return_types.emplace_back(LogicalType::VARCHAR);

	names.emplace_back("config_oid");
	return_types.emplace_back(LogicalType::BIGINT);

	names.emplace_back("internal");
	return_types.emplace_back(LogicalType::BOOLEAN);

	names.emplace_back("temporary");
	return_types.emplace_back(LogicalType::BOOLEAN);

	names.emplace_back("config_value");
	return_types.emplace_back(LogicalType::VARCHAR);

	return nullptr;
}

unique_ptr<GlobalTableFunctionState> VaultDBConfigsInit(ClientContext &context, TableFunctionInitInput &input) {
	auto result = make_uniq<VaultDBConfigsData>();

	// scan all the schemas for tables and collect themand collect them
	auto schemas = Catalog::GetAllSchemas(context);
	for (auto &schema : schemas) {
		schema.get().Scan(context, CatalogType::CONFIG_ENTRY,
		                  [&](CatalogEntry &entry) { result->entries.push_back(entry); });
	};
	return std::move(result);
}

void VaultDBConfigsFunction(ClientContext &context, TableFunctionInput &data_p, DataChunk &output) {
	auto &data = data_p.global_state->Cast<VaultDBConfigsData>();
	if (data.offset >= data.entries.size()) {
		// finished returning values
		return;
	}
	// start returning values
	// either fill up the chunk or return all the remaining columns
	idx_t count = 0;
	while (data.offset < data.entries.size() && count < STANDARD_VECTOR_SIZE) {
		auto &entry = data.entries[data.offset++].get();

		if (entry.type != CatalogType::CONFIG_ENTRY) {
			continue;
		}
		auto &config = entry.Cast<ConfigCatalogEntry>();
		// return values:
		idx_t col = 0;
		// database_name, VARCHAR
		output.SetValue(col++, count, config.catalog.GetName());
		// database_oid, BIGINT
		output.SetValue(col++, count, Value::BIGINT(config.catalog.GetOid()));
		// schema_name, LogicalType::VARCHAR
		output.SetValue(col++, count, Value(config.schema.name));
		// schema_oid, LogicalType::BIGINT
		output.SetValue(col++, count, Value::BIGINT(config.schema.oid));
		// tag_name, LogicalType::VARCHAR
		output.SetValue(col++, count, Value(config.name));
		// tag_oid, LogicalType::BIGINT
		output.SetValue(col++, count, Value::BIGINT(config.oid));
		// internal, LogicalType::BOOLEAN
		output.SetValue(col++, count, Value::BOOLEAN(config.internal));
		// temporary, LogicalType::BOOLEAN
		output.SetValue(col++, count, Value::BOOLEAN(config.temporary));
		// comment, LogicalType::VARCHAR
		output.SetValue(col++, count, Value(config.value));

		count++;
	}
	output.SetCardinality(count);
}

void VaultDBConfigsFun::RegisterFunction(BuiltinFunctions &set) {
	set.AddFunction(TableFunction("vaultdb_configs", {}, VaultDBConfigsFunction, VaultDBConfigsBind, VaultDBConfigsInit));
}

} // namespace duckdb
