//===----------------------------------------------------------------------===//
//                         DuckDB
//
// duckdb/execution/operator/schema/physical_create_tag.hpp
//
//
//===----------------------------------------------------------------------===//

#pragma once

#include "duckdb/execution/physical_operator.hpp"
#include "duckdb/parser/parsed_data/create_tag_info.hpp"

namespace duckdb {

//! PhysicalCreateTag represents a CREATE TAG command
class PhysicalCreateTag : public PhysicalOperator {
public:
	explicit PhysicalCreateTag(unique_ptr<CreateTagInfo> info, idx_t estimated_cardinality)
	    : PhysicalOperator(PhysicalOperatorType::CREATE_TAG, {LogicalType::BIGINT}, estimated_cardinality),
	      info(std::move(info)) {
	}

	unique_ptr<CreateTagInfo> info;

public:
	SourceResultType GetData(ExecutionContext &context, DataChunk &chunk, OperatorSourceInput &input) const override;

	bool IsSource() const override {
		return true;
	}
};

} // namespace duckdb
