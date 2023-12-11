#include "duckdb/catalog/catalog_entry/table_catalog_entry.hpp"
#include "duckdb/catalog/catalog_entry/table_function_catalog_entry.hpp"
#include "duckdb/execution/operator/join/physical_hash_merge.hpp"
#include "duckdb/execution/operator/join/physical_merge.hpp"
#include "duckdb/execution/operator/projection/physical_projection.hpp"
#include "duckdb/execution/operator/projection/physical_tableinout_function.hpp"
#include "duckdb/execution/operator/scan/physical_table_scan.hpp"
#include "duckdb/execution/physical_plan_generator.hpp"
#include "duckdb/function/table/table_scan.hpp"
#include "duckdb/main/client_context.hpp"
#include "duckdb/main/config.hpp"
#include "duckdb/planner/expression/bound_constant_expression.hpp"
#include "duckdb/planner/expression/bound_reference_expression.hpp"
#include "duckdb/planner/operator/logical_merge.hpp"

namespace duckdb {

unique_ptr<PhysicalOperator> PhysicalPlanGenerator::CreatePlan(LogicalMerge &op) {
	auto table = op.GetTable();
	unique_ptr<TableFilterSet> table_filters;
	if (!op.table_filters.filters.empty()) { // TODO: Add partition key filters for merge operation
		table_filters = CreateTableFilterSet(op.table_filters, op.column_ids);
	}
	if (op.parquet_function.dependency) {
		op.parquet_function.dependency(dependencies, op.parquet_bind_data.get());
	}
	ExtraOperatorInfo extra_info; //! VAULTDB: Add extra info to filter specific files etc.
	auto right = make_uniq<PhysicalTableScan>(op.types, op.parquet_function, std::move(op.parquet_bind_data),
	                                          op.returned_types, op.column_ids, op.projection_ids, op.names,
	                                          std::move(table_filters), op.estimated_cardinality, extra_info);
	auto left = CreatePlan(op.Cast<LogicalGet>());
	D_ASSERT(left && right);

	vector<column_t> merge_key_column_ids = op.BuildMergeKeyColumnIds();
	return make_uniq<PhysicalMerge>(op.types, table->GetStorage(), std::move(left), std::move(right),
	                                std::move(merge_key_column_ids), op.estimated_cardinality);
}

} // namespace duckdb
