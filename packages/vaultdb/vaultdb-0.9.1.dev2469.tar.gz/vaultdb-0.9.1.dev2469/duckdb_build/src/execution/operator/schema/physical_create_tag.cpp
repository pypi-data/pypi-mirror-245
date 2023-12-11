#include "duckdb/execution/operator/schema/physical_create_tag.hpp"

#include "duckdb/catalog/catalog.hpp"

namespace duckdb {

//===--------------------------------------------------------------------===//
// Source
//===--------------------------------------------------------------------===//
SourceResultType PhysicalCreateTag::GetData(ExecutionContext &context, DataChunk &chunk,
                                            OperatorSourceInput &input) const {
	auto &catalog = Catalog::GetCatalog(context.client, info->catalog);
	catalog.CreateTag(context.client, *info);
	return SourceResultType::FINISHED;
}

} // namespace duckdb
