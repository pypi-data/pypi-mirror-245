//===----------------------------------------------------------------------===//
//                         DuckDB
//
// duckdb/execution/operator/schema/physical_role_sequence.hpp
//
//
//===----------------------------------------------------------------------===//

#pragma once

#include "duckdb/execution/physical_operator.hpp"
#include "duckdb/parser/parsed_data/create_fortress_info.hpp"

namespace duckdb {

//! PhysicalCreateFortress represents a CREATE ROLE command
class PhysicalCreateFortress : public PhysicalOperator {
public:
	explicit PhysicalCreateFortress(unique_ptr<CreateFortressInfo> info, idx_t estimated_cardinality)
	    : PhysicalOperator(PhysicalOperatorType::CREATE_FORTRESS, {LogicalType::BIGINT}, estimated_cardinality),
	      info(std::move(info)) {
	}

	unique_ptr<CreateFortressInfo> info;

public:
	// Source interface
	SourceResultType GetData(ExecutionContext &context, DataChunk &chunk, OperatorSourceInput &input) const override;

	bool IsSource() const override {
		return true;
	}
};

} // namespace duckdb
