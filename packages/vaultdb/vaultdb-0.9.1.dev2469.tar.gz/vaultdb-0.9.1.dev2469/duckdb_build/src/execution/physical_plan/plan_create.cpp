#include "duckdb/execution/operator/schema/physical_create_function.hpp"
#include "duckdb/execution/operator/schema/physical_create_schema.hpp"
#include "duckdb/execution/operator/schema/physical_create_sequence.hpp"
#include "duckdb/execution/operator/schema/physical_create_role.hpp"
#include "duckdb/execution/operator/schema/physical_create_tag.hpp"
#include "duckdb/execution/operator/schema/physical_create_config.hpp"
#include "duckdb/execution/operator/schema/physical_create_fortress.hpp"
#include "duckdb/execution/operator/schema/physical_create_type.hpp"
#include "duckdb/execution/operator/schema/physical_create_view.hpp"
#include "duckdb/execution/physical_plan_generator.hpp"
#include "duckdb/parser/parsed_data/create_type_info.hpp"
#include "duckdb/planner/logical_operator.hpp"
#include "duckdb/planner/operator/logical_create.hpp"

namespace duckdb {

unique_ptr<PhysicalOperator> PhysicalPlanGenerator::CreatePlan(LogicalCreate &op) {
	switch (op.type) {
	case LogicalOperatorType::LOGICAL_CREATE_SEQUENCE:
		return make_uniq<PhysicalCreateSequence>(unique_ptr_cast<CreateInfo, CreateSequenceInfo>(std::move(op.info)),
		                                         op.estimated_cardinality);
	case LogicalOperatorType::LOGICAL_CREATE_ROLE:
		return make_uniq<PhysicalCreateRole>(unique_ptr_cast<CreateInfo, CreateRoleInfo>(std::move(op.info)),
		                                           op.estimated_cardinality);
	case LogicalOperatorType::LOGICAL_CREATE_TAG:
		return make_uniq<PhysicalCreateTag>(unique_ptr_cast<CreateInfo, CreateTagInfo>(std::move(op.info)),
		                                           op.estimated_cardinality);
	case LogicalOperatorType::LOGICAL_CREATE_CONFIG:
		return make_uniq<PhysicalCreateConfig>(unique_ptr_cast<CreateInfo, CreateConfigInfo>(std::move(op.info)),
		                                           op.estimated_cardinality);
	case LogicalOperatorType::LOGICAL_CREATE_FORTRESS:
		return make_uniq<PhysicalCreateFortress>(unique_ptr_cast<CreateInfo, CreateFortressInfo>(std::move(op.info)),
		                                           op.estimated_cardinality);
	case LogicalOperatorType::LOGICAL_CREATE_VIEW:
		return make_uniq<PhysicalCreateView>(unique_ptr_cast<CreateInfo, CreateViewInfo>(std::move(op.info)),
		                                     op.estimated_cardinality);
	case LogicalOperatorType::LOGICAL_CREATE_SCHEMA:
		return make_uniq<PhysicalCreateSchema>(unique_ptr_cast<CreateInfo, CreateSchemaInfo>(std::move(op.info)),
		                                       op.estimated_cardinality);
	case LogicalOperatorType::LOGICAL_CREATE_MACRO:
		return make_uniq<PhysicalCreateFunction>(unique_ptr_cast<CreateInfo, CreateMacroInfo>(std::move(op.info)),
		                                         op.estimated_cardinality);
	case LogicalOperatorType::LOGICAL_CREATE_TYPE: {
		unique_ptr<PhysicalOperator> create = make_uniq<PhysicalCreateType>(
		    unique_ptr_cast<CreateInfo, CreateTypeInfo>(std::move(op.info)), op.estimated_cardinality);
		if (!op.children.empty()) {
			D_ASSERT(op.children.size() == 1);
			auto plan = CreatePlan(*op.children[0]);
			create->children.push_back(std::move(plan));
		}
		return create;
	}
	default:
		throw NotImplementedException("Unimplemented type for logical simple create");
	}
}

} // namespace duckdb
