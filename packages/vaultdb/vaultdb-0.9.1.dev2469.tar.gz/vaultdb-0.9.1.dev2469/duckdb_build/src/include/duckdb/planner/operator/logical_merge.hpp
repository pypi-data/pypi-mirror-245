//===----------------------------------------------------------------------===//
//                         DuckDB
//
// duckdb/planner/operator/logical_merge.hpp
//
//
//===----------------------------------------------------------------------===//

#pragma once

#include "duckdb/planner/operator/logical_get.hpp"

namespace duckdb {

class TableCatalogEntry;

//! LogicalMerge represents a comibining remote and local data
class LogicalMerge : public LogicalGet {
public:
	static constexpr const LogicalOperatorType TYPE = LogicalOperatorType::LOGICAL_GET;

public:
	LogicalMerge(idx_t table_index, TableFunction function, unique_ptr<FunctionData> bind_data,
	             TableFunction parquet_function, unique_ptr<FunctionData> parquet_bind_data,
	             vector<LogicalType> returned_types, vector<string> returned_names);

	//! The function that is called
	TableFunction parquet_function;
	//! The bind data of the function
	unique_ptr<FunctionData> parquet_bind_data;
	//! primary key Indexes for remote and local data merge
	vector<column_t> merge_column_indexes;

private:
	vector<column_t> merge_key_column_ids;
	bool built_merge_keys = false;

public:
	//! VaultDB: Functions to read parquet files
	vector<column_t> BuildMergeKeyColumnIds();
	idx_t EstimateCardinality(ClientContext &context) override;

	void Serialize(Serializer &serializer) const override;
	static unique_ptr<LogicalOperator> Deserialize(Deserializer &deserializer);
};
} // namespace duckdb
