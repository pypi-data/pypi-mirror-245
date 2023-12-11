#include "duckdb/execution/operator/join/physical_hash_merge.hpp"

#include "duckdb/common/sort/sort.hpp"
#include "duckdb/common/types/value.hpp"
#include "duckdb/common/unordered_map.hpp"
#include "duckdb/execution/expression_executor.hpp"
#include "duckdb/main/client_context.hpp"
#include "duckdb/parallel/event.hpp"
#include "duckdb/parallel/meta_pipeline.hpp"
#include "duckdb/parallel/pipeline.hpp"
#include "duckdb/storage/buffer_manager.hpp"
#include "duckdb/storage/data_table.hpp"

namespace duckdb {

PhysicalHashMerge::PhysicalHashMerge(vector<LogicalType> types, DataTable &table, unique_ptr<PhysicalOperator> remote,
                                     unique_ptr<PhysicalOperator> local, vector<column_t> merge_key_column_idxs,
                                     idx_t estimated_cardinality)
    : PhysicalOperator(PhysicalOperatorType::MERGE_DATA, std::move(types), estimated_cardinality), table(table),
      merge_key_column_idxs(std::move(merge_key_column_idxs)) {
	children.push_back(std::move(local)); // Start with local first as we want to show local and remove remote
	children.push_back(std::move(remote));
}

//===--------------------------------------------------------------------===//
// Sink
//===--------------------------------------------------------------------===//
class MergeGlobalState : public GlobalSinkState {
public:
	explicit MergeGlobalState(ClientContext &context, DataTable &table) : final_reservoir(context), table(table) {
	}

	//! remote chunks
	ChunkCollection final_reservoir;
	DataTable &table;
	//! hash values
	unordered_map<hash_t, bool> hash_map;

	bool finalized;

	void ScanMatches(const vector<column_t> &merge_key_column_idxs, DataChunk &input, DataChunk &result) {
		if (hash_map.size() == 0 && input.size() > 0)
			result.Reference(input);
		else if (input.size() > 0) {
			SelectionVector sel(input.size());
			idx_t result_count = 0;
			for (idx_t row_idx = 0; row_idx < input.size(); row_idx++) {
				hash_t hashvalue;
				bool combinehash = false;
				for (auto &col_idx : merge_key_column_idxs) {
					auto value = input.GetValue(col_idx, row_idx);
					if (combinehash) {
						auto hash_val = value.Hash();
						hashvalue = (hashvalue * UINT64_C(0xbf58476d1ce4e5b9)) ^ hash_val;
					} else {
						hashvalue = value.Hash();
						combinehash = true;
					}
				}
				if (hash_map.find(hashvalue) != hash_map.end())
					continue;
				if (table.info->tombstone && table.info->tombstone->Count() > 0) {
					vector<row_t> result_ids;
					table.info->tombstone->Search(Value::HASH(hashvalue), 1, result_ids);
					if (result_ids.size() > 0)
						continue;
				}
				// value doesn't exists
				sel.set_index(result_count++, row_idx);
			}
			if (result_count > 0) {
				result.Slice(input, sel, result_count);
			}
		}

		for (idx_t col_idx = input.ColumnCount(); col_idx < result.ColumnCount(); col_idx++) {
			switch (result.data[col_idx].GetVectorType()) {
			case VectorType::FLAT_VECTOR:
				for (idx_t i = 0; i < result.ColumnCount(); i++)
					FlatVector::SetNull(result.data[col_idx], i, true);
				break;
			case VectorType::CONSTANT_VECTOR:
				ConstantVector::SetNull(result.data[col_idx], true);
				break;
			default:
				throw InternalException("Invalid result vector type for nested min/max");
			}
		}
	}
};

class MergeLocalState : public LocalSinkState {
public:
	MergeLocalState() {
	}

public:
	DataChunk build_chunk;
	unordered_map<hash_t, bool> hash_map;
};

unique_ptr<GlobalSinkState> PhysicalHashMerge::GetGlobalSinkState(ClientContext &context) const {
	// Get the payload layout from the return types
	auto state = make_uniq<MergeGlobalState>(context, table);
	return std::move(state);
}

unique_ptr<LocalSinkState> PhysicalHashMerge::GetLocalSinkState(ExecutionContext &context) const {
	auto result = make_uniq<MergeLocalState>();
	result->build_chunk.Initialize(Allocator::Get(context.client), types);
	return std::move(result);
}

SinkResultType PhysicalHashMerge::Sink(ExecutionContext &context, DataChunk &chunk, OperatorSinkInput &input) const {
	auto &lstate = input.local_state.Cast<MergeLocalState>();

	chunk.Verify();
	lstate.build_chunk.Reset();
	lstate.build_chunk.SetCardinality(chunk);
	lstate.build_chunk.source = chunk.source;

	if (chunk.size() > 0) {
		for (idx_t i = 0; i < types.size(); i++) {
			lstate.build_chunk.data[i].Reference(chunk.data[i]);
		}

		if (chunk.source == DataSourceId::LOCAL) {
			lstate.hash_map.clear();
			for (idx_t row_idx = 0; row_idx < chunk.size(); row_idx++) {
				hash_t hashvalue;
				bool combinehash = false;
				for (auto &col_idx : merge_key_column_idxs) {
					auto value = chunk.GetValue(col_idx, row_idx);
					if (combinehash) {
						auto hash_val = value.Hash();
						hashvalue = (hashvalue * UINT64_C(0xbf58476d1ce4e5b9)) ^ hash_val;
					} else {
						hashvalue = value.Hash();
						combinehash = true;
					}
				}
				lstate.hash_map[hashvalue] = true;
			}
		}
	}

	return SinkResultType::NEED_MORE_INPUT;
}

SinkCombineResultType PhysicalHashMerge::Combine(ExecutionContext &context, OperatorSinkCombineInput &input) const {
	auto &gstate = input.global_state.Cast<MergeGlobalState>();
	auto &lstate = input.local_state.Cast<MergeLocalState>();
	if (lstate.build_chunk.size() == 0)
		return SinkCombineResultType::FINISHED;

	gstate.hash_map.insert(lstate.hash_map.begin(), lstate.hash_map.end());
	gstate.final_reservoir.Append(lstate.build_chunk);	
	return SinkCombineResultType::FINISHED;
}

SinkFinalizeType PhysicalHashMerge::Finalize(Pipeline &pipeline, Event &event, ClientContext &context,
	                          OperatorSinkFinalizeInput &input) const {
	auto &gstate = input.global_state.Cast<MergeGlobalState>();
	gstate.finalized = true;

	return SinkFinalizeType::READY;
}

//===--------------------------------------------------------------------===//
// Operator
//===--------------------------------------------------------------------===//
class PhysicalHashMergeState : public OperatorState {
public:
	explicit PhysicalHashMergeState() {
	}
};

unique_ptr<OperatorState> PhysicalHashMerge::GetOperatorState(ExecutionContext &context) const {
	auto state = make_uniq<PhysicalHashMergeState>();
	return std::move(state);
}

OperatorResultType PhysicalHashMerge::Execute(ExecutionContext &context, DataChunk &input, DataChunk &chunk,
                                              GlobalOperatorState &gstate_p, OperatorState &state_p) const {
	// auto &state = (PhysicalHashMergeState &)state_p;
	auto &gstate = (MergeGlobalState &)*sink_state;

	if (gstate.final_reservoir.ChunkCount() == 0 && input.size() == 0)
		return OperatorResultType::FINISHED;

	if (gstate.final_reservoir.ChunkCount() > 0) {
		auto chunk_ptr = gstate.final_reservoir.PopChunk();
		if (chunk_ptr)
			chunk.Reference(*chunk_ptr);

		if (input.size() == 0)
			return OperatorResultType::NEED_MORE_INPUT;

		return OperatorResultType::HAVE_MORE_OUTPUT;
	}

	gstate.ScanMatches(merge_key_column_idxs, input, chunk);

	return OperatorResultType::NEED_MORE_INPUT;
}

//===--------------------------------------------------------------------===//
// Source
//===--------------------------------------------------------------------===//
class HashMergeScanState : public GlobalSourceState {
public:
	explicit HashMergeScanState(const PhysicalHashMerge &op) : op(op) {
	}
	const PhysicalHashMerge &op;
};

unique_ptr<GlobalSourceState> PhysicalHashMerge::GetGlobalSourceState(ClientContext &context) const {
	return make_uniq<HashMergeScanState>(*this);
}

SourceResultType PhysicalHashMerge::GetData(ExecutionContext &context, DataChunk &chunk,
                                            OperatorSourceInput &input) const {
	auto &sink = (MergeGlobalState &)*sink_state;

	if (chunk.size() > 0 && chunk.source == DataSourceId::REMOTE) {
		DataChunk result;
		sink.ScanMatches(merge_key_column_idxs, chunk, result);
		chunk.Reference(result);
	} else if (sink.final_reservoir.ChunkCount() > 0) {
		auto chunk_ptr = sink.final_reservoir.PopChunk();
		if (chunk_ptr)
			chunk.Reference(*chunk_ptr);
	}
	return SourceResultType::FINISHED;
}

//===--------------------------------------------------------------------===//
// Pipeline Construction
//===--------------------------------------------------------------------===//
void PhysicalHashMerge::BuildPipelines(Pipeline &current, MetaPipeline &meta_pipeline) {
	D_ASSERT(children.size() == 2);

	// Build the LHS
	op_state.reset();
	sink_state.reset();

	// 'current' is the probe pipeline: add this operator
	auto &state = meta_pipeline.GetState();
	state.AddPipelineOperator(current, *this);

	// save the last added pipeline to set up dependencies later (in case we need to add a child pipeline)
	vector<shared_ptr<Pipeline>> pipelines_so_far;
	meta_pipeline.GetPipelines(pipelines_so_far, false);
	auto last_pipeline = pipelines_so_far.back().get();

	// on the RHS (build side), we construct a child MetaPipeline with this operator as its sink
	auto &child_meta_pipeline = meta_pipeline.CreateChildMetaPipeline(current, *this);
	child_meta_pipeline.Build(*children[1]);

	// continue building the current pipeline on the LHS (probe side)
	children[0]->BuildPipelines(current, meta_pipeline);

	meta_pipeline.CreateChildPipeline(current, *this, last_pipeline);
}

vector<const_reference<PhysicalOperator>> PhysicalHashMerge::GetSources() const {
	return {*this};
}

} // namespace duckdb
