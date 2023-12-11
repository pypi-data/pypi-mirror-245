#include "duckdb/parser/parsed_data/create_config_info.hpp"
#include "duckdb/common/helper.hpp"

namespace duckdb {

unique_ptr<CreateInfo> CreateConfigInfo::Copy() const {
	auto result = make_uniq<CreateConfigInfo>();
	CopyProperties(*result);
	result->name = name;
	result->value = value;
	return std::move(result);
}

} // namespace duckdb
