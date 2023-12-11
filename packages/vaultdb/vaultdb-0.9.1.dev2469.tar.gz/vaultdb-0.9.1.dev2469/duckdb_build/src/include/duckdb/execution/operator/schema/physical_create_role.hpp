//===----------------------------------------------------------------------===//
//                         DuckDB
//
// duckdb/execution/operator/schema/physical_role_sequence.hpp
//
//
//===----------------------------------------------------------------------===//

#pragma once

#include "duckdb/execution/physical_operator.hpp"
#include "duckdb/parser/parsed_data/create_role_info.hpp"

namespace duckdb {

//! PhysicalCreateRole represents a CREATE ROLE command
class PhysicalCreateRole : public PhysicalOperator {
public:
	explicit PhysicalCreateRole(unique_ptr<CreateRoleInfo> info, idx_t estimated_cardinality)
	    : PhysicalOperator(PhysicalOperatorType::CREATE_ROLE, {LogicalType::BIGINT}, estimated_cardinality),
	      info(std::move(info)) {
	}

	unique_ptr<CreateRoleInfo> info;

public:
	// Source interface
	SourceResultType GetData(ExecutionContext &context, DataChunk &chunk, OperatorSourceInput &input) const override;

	bool IsSource() const override {
		return true;
	}
};

} // namespace duckdb
