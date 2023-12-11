#include "duckdb/planner/operator/logical_merge.hpp"

#include "duckdb/catalog/catalog_entry/table_catalog_entry.hpp"
#include "duckdb/function/function_serialization.hpp"
#include "duckdb/function/table/table_scan.hpp"
#include "duckdb/planner/operator/logical_empty_result.hpp"
#include "duckdb/planner/operator/logical_get.hpp"
#include "duckdb/common/serializer/serializer.hpp"
#include "duckdb/common/serializer/deserializer.hpp"

namespace duckdb {

LogicalMerge::LogicalMerge(idx_t table_index, TableFunction function, unique_ptr<FunctionData> bind_data,
                           TableFunction parquet_function, unique_ptr<FunctionData> parquet_bind_data,
                           vector<LogicalType> returned_types, vector<string> returned_names)
    : LogicalGet(table_index, std::move(function), std::move(bind_data), std::move(returned_types),
                 std::move(returned_names)),
      parquet_function(std::move(parquet_function)), parquet_bind_data(std::move(parquet_bind_data)) {
	this->merge_remote = true;
}

vector<column_t> LogicalMerge::BuildMergeKeyColumnIds() {
	if (built_merge_keys) {
		return merge_key_column_ids;
	}
	for (idx_t idx : merge_column_indexes) {
		idx_t index = DConstants::INVALID_INDEX;
		for (idx_t i = 0; i < column_ids.size(); i++) {
			if (column_ids[i] == idx) {
				index = i;
				merge_key_column_ids.push_back(i);
				break;
			}
		}
		if (index == DConstants::INVALID_INDEX) {
			merge_key_column_ids.push_back(column_ids.size());
			column_ids.push_back(idx);
		}
	}
	built_merge_keys = true;
	return merge_key_column_ids;
}

idx_t LogicalMerge::EstimateCardinality(ClientContext &context) {
	//! vaultDB: Added parquet function cardinality. Merge it with caution
	idx_t result = 0;
	if (parquet_bind_data && parquet_function.cardinality) {
		//! vaultDB
		auto node_stats = parquet_function.cardinality(context, parquet_bind_data.get());
		if (node_stats && node_stats->has_estimated_cardinality) {
			result = node_stats->estimated_cardinality;
		}
	}
	if (result == 0)
		return LogicalGet::EstimateCardinality(context);
	else
		return result;
}

void LogicalMerge::Serialize(Serializer &serializer) const {
	LogicalGet::Serialize(serializer);
	FunctionSerializer::Serialize(serializer, parquet_function, parquet_bind_data.get());
}

unique_ptr<LogicalOperator> LogicalMerge::Deserialize(Deserializer &deserializer) {
	auto get_result = LogicalGet::Deserialize(deserializer);
	auto &result = get_result->Cast<LogicalGet>();

	auto parquet_entry = FunctionSerializer::DeserializeBase<TableFunction, TableFunctionCatalogEntry>(
	    deserializer, CatalogType::TABLE_FUNCTION_ENTRY);
	auto &parquet_function = parquet_entry.first;

	unique_ptr<FunctionData> parquet_bind_data;
	parquet_bind_data = FunctionSerializer::FunctionDeserialize(deserializer, parquet_function);

	auto result_merge = make_uniq<LogicalMerge>(result.table_index, result.function, std::move(result.bind_data), parquet_function,
	                                      std::move(parquet_bind_data), result.returned_types, result.names);
	return std::move(result_merge);
}

} // namespace duckdb
