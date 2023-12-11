#include "duckdb/catalog/catalog.hpp"
#include "duckdb/catalog/catalog_entry/schema_catalog_entry.hpp"
#include "duckdb/catalog/catalog_entry/role_catalog_entry.hpp"
#include "duckdb/common/exception.hpp"
#include "duckdb/function/table/system_functions.hpp"
#include "duckdb/main/client_context.hpp"
#include "duckdb/main/client_data.hpp"
#include "duckdb/parser/constraint.hpp"
#include "duckdb/parser/constraints/unique_constraint.hpp"
#include "duckdb/storage/data_table.hpp"
#include "duckdb/storage/table_storage_info.hpp"

namespace duckdb {

struct VaultDBPrivilegesData : public GlobalTableFunctionState {
	VaultDBPrivilegesData() : offset(0) {
	}

	vector<reference<CatalogEntry>> entries;
	idx_t offset;
};

static unique_ptr<FunctionData> VaultDBPrivilegesBind(ClientContext &context, TableFunctionBindInput &input,
                                                 vector<LogicalType> &return_types, vector<string> &names) {
	names.emplace_back("database_name");
	return_types.emplace_back(LogicalType::VARCHAR);

	names.emplace_back("database_oid");
	return_types.emplace_back(LogicalType::BIGINT);

	names.emplace_back("schema_name");
	return_types.emplace_back(LogicalType::VARCHAR);

	names.emplace_back("schema_oid");
	return_types.emplace_back(LogicalType::BIGINT);

	names.emplace_back("role_name");
	return_types.emplace_back(LogicalType::VARCHAR);

	names.emplace_back("role_oid");
	return_types.emplace_back(LogicalType::BIGINT);

	names.emplace_back("internal");
	return_types.emplace_back(LogicalType::BOOLEAN);

	names.emplace_back("temporary");
	return_types.emplace_back(LogicalType::BOOLEAN);

	names.emplace_back("resource_type");
	return_types.emplace_back(LogicalType::VARCHAR);

	names.emplace_back("resource_name");
	return_types.emplace_back(LogicalType::VARCHAR);

	names.emplace_back("grantOption");
	return_types.emplace_back(LogicalType::BOOLEAN);

	names.emplace_back("unauthorized_columns");
	return_types.emplace_back(LogicalType::LIST(LogicalType::VARCHAR));

	return nullptr;
}

unique_ptr<GlobalTableFunctionState> VaultDBPrivilegesInit(ClientContext &context, TableFunctionInitInput &input) {
	auto result = make_uniq<VaultDBPrivilegesData>();

	// scan all the schemas for tables and collect themand collect them
	auto schemas = Catalog::GetAllSchemas(context);
	for (auto &schema : schemas) {
		schema.get().Scan(context, CatalogType::ROLE_ENTRY,
		                  [&](CatalogEntry &entry) { result->entries.push_back(entry); });
	};
	return std::move(result);
}

void VaultDBPrivilegesFunction(ClientContext &context, TableFunctionInput &data_p, DataChunk &output) {
	auto &data = data_p.global_state->Cast<VaultDBPrivilegesData>();
	if (data.offset >= data.entries.size()) {
		// finished returning values
		return;
	}
	// start returning values
	// either fill up the chunk or return all the remaining columns
	idx_t count = 0;
	while (data.offset < data.entries.size() && count < STANDARD_VECTOR_SIZE) {
		auto &entry = data.entries[data.offset++].get();

		if (entry.type != CatalogType::ROLE_ENTRY) {
			continue;
		}
		auto &role = entry.Cast<RoleCatalogEntry>();
		for (auto &privilegetype: role.info->privileges)
		{
			for (auto &privilege: privilegetype.second)
			{
				// return values:
				idx_t col = 0;
				// database_name, VARCHAR
				output.SetValue(col++, count, role.catalog.GetName());
				// database_oid, BIGINT
				output.SetValue(col++, count, Value::BIGINT(role.catalog.GetOid()));
				// schema_name, LogicalType::VARCHAR
				output.SetValue(col++, count, Value(role.schema.name));
				// schema_oid, LogicalType::BIGINT
				output.SetValue(col++, count, Value::BIGINT(role.schema.oid));
				// role_name, LogicalType::VARCHAR
				output.SetValue(col++, count, Value(role.info->name));
				// role_oid, LogicalType::BIGINT
				output.SetValue(col++, count, Value::BIGINT(role.oid));
				// internal, LogicalType::BOOLEAN
				output.SetValue(col++, count, Value::BOOLEAN(role.internal));
				// temporary, LogicalType::BOOLEAN
				output.SetValue(col++, count, Value::BOOLEAN(role.temporary));
				// resource_type, LogicalType::VARCHAR
				output.SetValue(col++, count, Value(CatalogTypeToString(privilegetype.first)));
				// resource_name, LogicalType::VARCHAR
				output.SetValue(col++, count, Value(privilege.first));
				// grantOption, LogicalType::BOOLEAN
				output.SetValue(col++, count, Value(privilege.second->grantOption));
				
				vector<Value> results;
				for (auto val : privilege.second->unauthorized_columns) {
					results.emplace_back(Value(val));
				}
				// unauthorized_columns, LogicalType::LIST
				output.SetValue(col++, count, Value::LIST(std::move(results)));

				count++;
			}
		}
	}
	output.SetCardinality(count);
}

void VaultDBPrivilegesFun::RegisterFunction(BuiltinFunctions &set) {
	set.AddFunction(TableFunction("vaultdb_privileges", {}, VaultDBPrivilegesFunction, VaultDBPrivilegesBind, VaultDBPrivilegesInit));
}

} // namespace duckdb
