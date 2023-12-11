#include "duckdb/execution/operator/schema/physical_create_config.hpp"

#include "duckdb/catalog/catalog.hpp"

namespace duckdb {

//===--------------------------------------------------------------------===//
// Source
//===--------------------------------------------------------------------===//
SourceResultType PhysicalCreateConfig::GetData(ExecutionContext &context, DataChunk &chunk,
                                            OperatorSourceInput &input) const {
	auto &catalog = Catalog::GetCatalog(context.client, info->catalog);
	catalog.CreateConfig(context.client, *info);
	return SourceResultType::FINISHED;
}

} // namespace duckdb
