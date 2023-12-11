#include "duckdb/execution/operator/schema/physical_create_fortress.hpp"

#include "duckdb/catalog/catalog.hpp"

namespace duckdb {

//===--------------------------------------------------------------------===//
// Source
//===--------------------------------------------------------------------===//
SourceResultType PhysicalCreateFortress::GetData(ExecutionContext &context, DataChunk &chunk,
                                                 OperatorSourceInput &input) const {
	auto &catalog = Catalog::GetCatalog(context.client, info->catalog);
	catalog.CreateFortress(context.client, *info);
	return SourceResultType::FINISHED;
}

} // namespace duckdb
