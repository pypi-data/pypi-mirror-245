#include "duckdb/parser/parsed_data/create_fortress_info.hpp"

#include "duckdb/common/helper.hpp"

namespace duckdb {

unique_ptr<CreateInfo> CreateFortressInfo::Copy() const {
	auto result = make_uniq<CreateFortressInfo>();
	CopyProperties(*result);
	result->name = name;
	result->locked = locked;
	result->start_date = start_date;
	result->end_date = end_date;
	result->unlocked_for_role = unlocked_for_role;
	result->table = table->Copy();
	result->expression = expression->Copy();
	result->expression = complement_expression->Copy();
	return std::move(result);
}

} // namespace duckdb
