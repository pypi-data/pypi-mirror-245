//===----------------------------------------------------------------------===//
//                         DuckDB
//
// duckdb/execution/operator/join/physical_merge.hpp
//
//
//===----------------------------------------------------------------------===//

#pragma once

#include "duckdb/common/types/chunk_collection.hpp"
#include "duckdb/common/types/column/column_data_collection.hpp"
#include "duckdb/execution/physical_operator.hpp"

namespace duckdb {

class DataTable;

//! PhysicalMerge represents a merge from parquet and local data
class PhysicalMerge : public PhysicalOperator {
public:
	PhysicalMerge(vector<LogicalType> types, DataTable &table, unique_ptr<PhysicalOperator> local,
	              unique_ptr<PhysicalOperator> remote, vector<column_t> merge_key_column_idxs,
	              idx_t estimated_cardinality);

	DataTable &table;
	vector<column_t> merge_key_column_idxs;

public:
	// Operator Interface
	OperatorResultType Execute(ExecutionContext &context, DataChunk &input, DataChunk &chunk,
	                           GlobalOperatorState &gstate, OperatorState &state) const override;

public:
	// Source interface
	SourceResultType GetData(ExecutionContext &context, DataChunk &chunk, OperatorSourceInput &input) const override;

	bool IsSource() const override {
		return true;
	}

public:
	// Sink Interface
	unique_ptr<GlobalSinkState> GetGlobalSinkState(ClientContext &context) const override;
	SinkResultType Sink(ExecutionContext &context, DataChunk &chunk, OperatorSinkInput &input) const override;

	bool IsSink() const override {
		return true;
	}

public:
	void BuildPipelines(Pipeline &current, MetaPipeline &meta_pipeline) override;
	vector<const_reference<PhysicalOperator>> GetSources() const override;
};
} // namespace duckdb
