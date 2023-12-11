#include "duckdb/parser/parsed_data/create_tag_info.hpp"
#include "duckdb/common/helper.hpp"

namespace duckdb {

unique_ptr<CreateInfo> CreateTagInfo::Copy() const {
	auto result = make_uniq<CreateTagInfo>();
	CopyProperties(*result);
	result->name = name;
	result->comment = comment;
	result->function = function->Copy();
	return std::move(result);
}

} // namespace duckdb
