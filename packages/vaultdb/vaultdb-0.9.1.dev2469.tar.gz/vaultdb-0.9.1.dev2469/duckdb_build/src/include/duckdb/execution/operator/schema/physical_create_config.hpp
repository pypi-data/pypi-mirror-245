//===----------------------------------------------------------------------===//
//                         DuckDB
//
// duckdb/execution/operator/schema/physical_create_config.hpp
//
//
//===----------------------------------------------------------------------===//

#pragma once

#include "duckdb/execution/physical_operator.hpp"
#include "duckdb/parser/parsed_data/create_config_info.hpp"

namespace duckdb {

//! PhysicalCreateConfig represents a CREATE CONFIG command
class PhysicalCreateConfig : public PhysicalOperator {
public:
	explicit PhysicalCreateConfig(unique_ptr<CreateConfigInfo> info, idx_t estimated_cardinality)
	    : PhysicalOperator(PhysicalOperatorType::CREATE_CONFIG, {LogicalType::BIGINT}, estimated_cardinality),
	      info(std::move(info)) {
	}

	unique_ptr<CreateConfigInfo> info;

public:
	SourceResultType GetData(ExecutionContext &context, DataChunk &chunk, OperatorSourceInput &input) const override;

	bool IsSource() const override {
		return true;
	}
};

} // namespace duckdb
