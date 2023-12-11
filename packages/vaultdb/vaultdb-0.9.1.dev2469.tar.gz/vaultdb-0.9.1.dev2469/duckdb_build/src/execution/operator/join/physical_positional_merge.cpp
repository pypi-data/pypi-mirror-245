#include "duckdb/common/sort/sort.hpp"
#include "duckdb/common/types/column/column_data_collection.hpp"
#include "duckdb/common/types/value.hpp"
#include "duckdb/common/unordered_map.hpp"
#include "duckdb/execution/expression_executor.hpp"
#include "duckdb/execution/operator/join/physical_join.hpp"
#include "duckdb/execution/operator/join/physical_merge.hpp"
#include "duckdb/main/client_context.hpp"
#include "duckdb/parallel/event.hpp"
#include "duckdb/parallel/meta_pipeline.hpp"
#include "duckdb/parallel/pipeline.hpp"
#include "duckdb/storage/buffer_manager.hpp"
#include "duckdb/storage/data_table.hpp"

namespace duckdb {

PhysicalMerge::PhysicalMerge(vector<LogicalType> types, DataTable &table, unique_ptr<PhysicalOperator> remote,
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
class PhysicalMergeGlobalState : public GlobalSinkState {
public:
	PhysicalMergeGlobalState(ClientContext &context, const PhysicalMerge &op)
	    : final_reservoir(context), table(op.table), merge_key_column_idxs(std::move(op.merge_key_column_idxs)),
	      types(std::move(op.GetTypes())), finished(false) {
	}

	//! remote chunks
	ChunkCollection final_reservoir;
	DataTable &table;
	vector<column_t> merge_key_column_idxs;
	//! The types of the stored entries
	vector<LogicalType> types;
	mutex append_lock;
	//! hash values
	unordered_map<hash_t, bool> hash_map;

	bool finished;

	hash_t CalculateHash(idx_t row_idx, DataChunk &input) {
		hash_t result;
		bool combinehash = false;
		for (auto &col_idx : merge_key_column_idxs) {
			auto value = input.GetValue(col_idx, row_idx);
			if (combinehash) {
				auto hash_val = value.Hash();
				result = (result * UINT64_C(0xbf58476d1ce4e5b9)) ^ hash_val;
			} else {
				result = value.Hash();
				combinehash = true;
			}
		}
		return result;
	}

	void Append(ClientContext &context, DataChunk &input) {
		DataChunk build_chunk;
		build_chunk.Reset();
		build_chunk.SetCardinality(input);
		build_chunk.source = input.source;
		build_chunk.Initialize(context, types, input.size());

		if (input.size() > 0) {
			for (idx_t i = 0; i < types.size(); i++) {
				build_chunk.data[i].Reference(input.data[i]);
			}

			if (input.source == DataSourceId::LOCAL) {
				for (idx_t row_idx = 0; row_idx < input.size(); row_idx++) {
					hash_t hashvalue = CalculateHash(row_idx, input);
					hash_map[hashvalue] = true;
				}
			}
		}

		final_reservoir.Append(build_chunk);
	}

	void ScanMatches(DataChunk &input, DataChunk &result) {
		if (hash_map.size() == 0 && table.info->tombstone && table.info->tombstone->Count() == 0 && input.size() > 0)
			result.Reference(input);
		else if (input.size() > 0) {
			SelectionVector sel(input.size());
			idx_t result_count = 0;
			for (idx_t row_idx = 0; row_idx < input.size(); row_idx++) {
				hash_t hashvalue = CalculateHash(row_idx, input);
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
	}
};

unique_ptr<GlobalSinkState> PhysicalMerge::GetGlobalSinkState(ClientContext &context) const {
	return make_uniq<PhysicalMergeGlobalState>(context, *this);
}

SinkResultType PhysicalMerge::Sink(ExecutionContext &context, DataChunk &chunk, OperatorSinkInput &input) const {
	auto &sink = input.global_state.Cast<PhysicalMergeGlobalState>();
	chunk.Verify();
	lock_guard<mutex> client_guard(sink.append_lock);
	sink.Append(context.client, chunk);
	return SinkResultType::NEED_MORE_INPUT;
}

OperatorResultType PhysicalMerge::Execute(ExecutionContext &context, DataChunk &input, DataChunk &chunk,
                                          GlobalOperatorState &gstate, OperatorState &state_p) const {
	auto &sink = (PhysicalMergeGlobalState &)*sink_state;
	lock_guard<mutex> client_guard(sink.append_lock);
	sink.ScanMatches(input, chunk);
	return OperatorResultType::NEED_MORE_INPUT;
}

//===--------------------------------------------------------------------===//
// Source
//===--------------------------------------------------------------------===//
SourceResultType PhysicalMerge::GetData(ExecutionContext &context, DataChunk &chunk, OperatorSourceInput &input) const {
	auto &sink = (PhysicalMergeGlobalState &)*sink_state;
	lock_guard<mutex> client_guard(sink.append_lock);
	if (chunk.size() > 0 && chunk.source == DataSourceId::REMOTE) {
		DataChunk scanned_result;
		sink.ScanMatches(chunk, scanned_result);
		chunk.Reference(scanned_result);
		return SourceResultType::HAVE_MORE_OUTPUT;
	} else if (sink.final_reservoir.ChunkCount() > 0) {
		auto result_ptr = sink.final_reservoir.PopChunk();
		if (result_ptr) {
			if (result_ptr->source == DataSourceId::REMOTE) {
				DataChunk scanned_result;
				sink.ScanMatches(chunk, scanned_result);
				chunk.Reference(scanned_result);
			} else
				chunk.Reference(*result_ptr);
		}
		return SourceResultType::HAVE_MORE_OUTPUT;
	}
	return SourceResultType::FINISHED;
}

//===--------------------------------------------------------------------===//
// Pipeline Construction
//===--------------------------------------------------------------------===//
void PhysicalMerge::BuildPipelines(Pipeline &current, MetaPipeline &meta_pipeline) {
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

	// Positional joins are always outer
	meta_pipeline.CreateChildPipeline(current, *this, last_pipeline);
}

vector<const_reference<PhysicalOperator>> PhysicalMerge::GetSources() const {
	auto result = children[0]->GetSources();
	if (IsSource()) {
		result.push_back(*this);
	}
	return result;
}

} // namespace duckdb
