#include "duckdb/catalog/catalog.hpp"
#include "duckdb/catalog/catalog_entry/schema_catalog_entry.hpp"
#include "duckdb/catalog/catalog_entry/tag_catalog_entry.hpp"
#include "duckdb/common/exception.hpp"
#include "duckdb/function/table/system_functions.hpp"
#include "duckdb/main/client_context.hpp"
#include "duckdb/main/client_data.hpp"
#include "duckdb/parser/constraint.hpp"
#include "duckdb/parser/constraints/unique_constraint.hpp"
#include "duckdb/storage/data_table.hpp"
#include "duckdb/storage/table_storage_info.hpp"

namespace duckdb {

struct VaultDBTagsData : public GlobalTableFunctionState {
	VaultDBTagsData() : offset(0) {
	}

	vector<reference<CatalogEntry>> entries;
	idx_t offset;
};

static unique_ptr<FunctionData> VaultDBTagsBind(ClientContext &context, TableFunctionBindInput &input,
                                                 vector<LogicalType> &return_types, vector<string> &names) {
	names.emplace_back("database_name");
	return_types.emplace_back(LogicalType::VARCHAR);

	names.emplace_back("database_oid");
	return_types.emplace_back(LogicalType::BIGINT);

	names.emplace_back("schema_name");
	return_types.emplace_back(LogicalType::VARCHAR);

	names.emplace_back("schema_oid");
	return_types.emplace_back(LogicalType::BIGINT);

	names.emplace_back("tag_name");
	return_types.emplace_back(LogicalType::VARCHAR);

	names.emplace_back("tag_oid");
	return_types.emplace_back(LogicalType::BIGINT);

	names.emplace_back("internal");
	return_types.emplace_back(LogicalType::BOOLEAN);

	names.emplace_back("temporary");
	return_types.emplace_back(LogicalType::BOOLEAN);

	names.emplace_back("comment");
	return_types.emplace_back(LogicalType::VARCHAR);

	names.emplace_back("function");
	return_types.emplace_back(LogicalType::VARCHAR);

	names.emplace_back("sql");
	return_types.emplace_back(LogicalType::VARCHAR);

	return nullptr;
}

unique_ptr<GlobalTableFunctionState> VaultDBTagsInit(ClientContext &context, TableFunctionInitInput &input) {
	auto result = make_uniq<VaultDBTagsData>();

	// scan all the schemas for tables and collect themand collect them
	auto schemas = Catalog::GetAllSchemas(context);
	for (auto &schema : schemas) {
		schema.get().Scan(context, CatalogType::TAG_ENTRY,
		                  [&](CatalogEntry &entry) { result->entries.push_back(entry); });
	};
	return std::move(result);
}

void VaultDBTagsFunction(ClientContext &context, TableFunctionInput &data_p, DataChunk &output) {
	auto &data = data_p.global_state->Cast<VaultDBTagsData>();
	if (data.offset >= data.entries.size()) {
		// finished returning values
		return;
	}
	// start returning values
	// either fill up the chunk or return all the remaining columns
	idx_t count = 0;
	while (data.offset < data.entries.size() && count < STANDARD_VECTOR_SIZE) {
		auto &entry = data.entries[data.offset++].get();

		if (entry.type != CatalogType::TAG_ENTRY) {
			continue;
		}
		auto &tag = entry.Cast<TagCatalogEntry>();
		// return values:
		idx_t col = 0;
		// database_name, VARCHAR
		output.SetValue(col++, count, tag.catalog.GetName());
		// database_oid, BIGINT
		output.SetValue(col++, count, Value::BIGINT(tag.catalog.GetOid()));
		// schema_name, LogicalType::VARCHAR
		output.SetValue(col++, count, Value(tag.schema.name));
		// schema_oid, LogicalType::BIGINT
		output.SetValue(col++, count, Value::BIGINT(tag.schema.oid));
		// tag_name, LogicalType::VARCHAR
		output.SetValue(col++, count, Value(tag.name));
		// tag_oid, LogicalType::BIGINT
		output.SetValue(col++, count, Value::BIGINT(tag.oid));
		// internal, LogicalType::BOOLEAN
		output.SetValue(col++, count, Value::BOOLEAN(tag.internal));
		// temporary, LogicalType::BOOLEAN
		output.SetValue(col++, count, Value::BOOLEAN(tag.temporary));
		// comment, LogicalType::VARCHAR
		output.SetValue(col++, count, Value(tag.comment));
		// function, LogicalType::VARCHAR
		output.SetValue(col++, count, Value(tag.function->ToString()));
		// sql, LogicalType::VARCHAR
		output.SetValue(col++, count, Value(tag.ToSQL()));

		count++;
	}
	output.SetCardinality(count);
}

void VaultDBTagsFun::RegisterFunction(BuiltinFunctions &set) {
	set.AddFunction(TableFunction("vaultdb_tags", {}, VaultDBTagsFunction, VaultDBTagsBind, VaultDBTagsInit));
}

} // namespace duckdb
