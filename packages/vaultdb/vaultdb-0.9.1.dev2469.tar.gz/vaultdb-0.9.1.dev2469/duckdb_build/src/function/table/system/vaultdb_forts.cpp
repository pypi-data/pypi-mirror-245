#include "duckdb/catalog/catalog.hpp"
#include "duckdb/catalog/catalog_entry/schema_catalog_entry.hpp"
#include "duckdb/catalog/catalog_entry/fortress_catalog_entry.hpp"
#include "duckdb/common/exception.hpp"
#include "duckdb/function/table/system_functions.hpp"
#include "duckdb/main/client_context.hpp"
#include "duckdb/main/client_data.hpp"
#include "duckdb/parser/constraint.hpp"
#include "duckdb/parser/constraints/unique_constraint.hpp"
#include "duckdb/storage/data_table.hpp"
#include "duckdb/storage/table_storage_info.hpp"

namespace duckdb {

struct VaultDBFortsData : public GlobalTableFunctionState {
	VaultDBFortsData() : offset(0) {
	}

	vector<reference<CatalogEntry>> entries;
	idx_t offset;
};

static unique_ptr<FunctionData> VaultDBFortsBind(ClientContext &context, TableFunctionBindInput &input,
                                                 vector<LogicalType> &return_types, vector<string> &names) {
	names.emplace_back("database_name");
	return_types.emplace_back(LogicalType::VARCHAR);

	names.emplace_back("database_oid");
	return_types.emplace_back(LogicalType::BIGINT);

	names.emplace_back("schema_name");
	return_types.emplace_back(LogicalType::VARCHAR);

	names.emplace_back("schema_oid");
	return_types.emplace_back(LogicalType::BIGINT);

	names.emplace_back("fortress_name");
	return_types.emplace_back(LogicalType::VARCHAR);

	names.emplace_back("fortress_oid");
	return_types.emplace_back(LogicalType::BIGINT);

	names.emplace_back("internal");
	return_types.emplace_back(LogicalType::BOOLEAN);

	names.emplace_back("temporary");
	return_types.emplace_back(LogicalType::BOOLEAN);

	names.emplace_back("locked");
	return_types.emplace_back(LogicalType::BOOLEAN);

	names.emplace_back("start_date");
	return_types.emplace_back(LogicalType::VARCHAR);

	names.emplace_back("end_date");
	return_types.emplace_back(LogicalType::VARCHAR);

	names.emplace_back("unlocked_for_role");
	return_types.emplace_back(LogicalType::VARCHAR);

	names.emplace_back("table_name");
	return_types.emplace_back(LogicalType::VARCHAR);

	names.emplace_back("condition");
	return_types.emplace_back(LogicalType::VARCHAR);

	names.emplace_back("sql");
	return_types.emplace_back(LogicalType::VARCHAR);

	return nullptr;
}

unique_ptr<GlobalTableFunctionState> VaultDBFortsInit(ClientContext &context, TableFunctionInitInput &input) {
	auto result = make_uniq<VaultDBFortsData>();

	// scan all the schemas for tables and collect themand collect them
	auto schemas = Catalog::GetAllSchemas(context);
	for (auto &schema : schemas) {
		schema.get().Scan(context, CatalogType::FORTRESS_ENTRY,
		                  [&](CatalogEntry &entry) { result->entries.push_back(entry); });
	};
	return std::move(result);
}

void VaultDBFortsFunction(ClientContext &context, TableFunctionInput &data_p, DataChunk &output) {
	auto &data = data_p.global_state->Cast<VaultDBFortsData>();
	if (data.offset >= data.entries.size()) {
		// finished returning values
		return;
	}
	// start returning values
	// either fill up the chunk or return all the remaining columns
	idx_t count = 0;
	while (data.offset < data.entries.size() && count < STANDARD_VECTOR_SIZE) {
		auto &entry = data.entries[data.offset++].get();

		if (entry.type != CatalogType::FORTRESS_ENTRY) {
			continue;
		}
		auto &fortress = entry.Cast<FortressCatalogEntry>();
		// return values:
		idx_t col = 0;
		// database_name, VARCHAR
		output.SetValue(col++, count, fortress.catalog.GetName());
		// database_oid, BIGINT
		output.SetValue(col++, count, Value::BIGINT(fortress.catalog.GetOid()));
		// schema_name, LogicalType::VARCHAR
		output.SetValue(col++, count, Value(fortress.schema.name));
		// schema_oid, LogicalType::BIGINT
		output.SetValue(col++, count, Value::BIGINT(fortress.schema.oid));
		// fortress_name, LogicalType::VARCHAR
		output.SetValue(col++, count, Value(fortress.name));
		// fortress_oid, LogicalType::BIGINT
		output.SetValue(col++, count, Value::BIGINT(fortress.oid));
		// internal, LogicalType::BOOLEAN
		output.SetValue(col++, count, Value::BOOLEAN(fortress.internal));
		// temporary, LogicalType::BOOLEAN
		output.SetValue(col++, count, Value::BOOLEAN(fortress.temporary));
		// locked, LogicalType::BOOL
		output.SetValue(col++, count, Value(fortress.locked));
		// start_date, LogicalType::DATE
		output.SetValue(col++, count, Value(fortress.start_date));
		// start_date, LogicalType::DATE
		output.SetValue(col++, count, Value(fortress.end_date));
		// unlocked_for_role, LogicalType::BOOL
		output.SetValue(col++, count, Value(fortress.unlocked_for_role));
		// table name, LogicalType::VARCHAR
		output.SetValue(col++, count, Value(fortress.table->ToString()));
		// where clause, LogicalType::VARCHAR
		output.SetValue(col++, count, Value(fortress.expression->ToString()));
		// sql, LogicalType::VARCHAR
		output.SetValue(col++, count, Value(fortress.ToSQL()));

		count++;
	}
	output.SetCardinality(count);
}

void VaultDBFortsFun::RegisterFunction(BuiltinFunctions &set) {
	set.AddFunction(TableFunction("vaultdb_forts", {}, VaultDBFortsFunction, VaultDBFortsBind, VaultDBFortsInit));
}

} // namespace duckdb
