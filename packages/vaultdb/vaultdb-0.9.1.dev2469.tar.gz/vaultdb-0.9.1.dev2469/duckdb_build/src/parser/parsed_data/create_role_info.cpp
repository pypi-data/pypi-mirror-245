#include "duckdb/parser/parsed_data/create_role_info.hpp"

#include "duckdb/common/helper.hpp"

namespace duckdb {

unique_ptr<CreatePrivilegeInfo> CreatePrivilegeInfo::CopyPrivilegeInfo() const {
	auto result = make_uniq<CreatePrivilegeInfo>(type, name);
	CopyProperties(*result);
	result->grantOption = grantOption;
	result->privileges = privileges;
	for (idx_t i = 0; i < unauthorized_columns.size(); i++)
		result->unauthorized_columns.push_back(unauthorized_columns[i]);
	return result;
}

unique_ptr<CreateRoleInfo> CreateRoleInfo::CopyRole() const {
	auto result = make_uniq<CreateRoleInfo>();
	CopyProperties(*result);
	result->name = name;
	result->login = login;
	result->superuser = superuser;
	result->schema = schema;
	for (auto &privilegetypes : privileges) {
		auto privilegetype = privilegetypes.first;
		for (auto &privilege : privilegetypes.second) {
			result->privileges[privilegetype][privilege.first] = privilege.second->CopyPrivilegeInfo();
		}
	}
	return result;
}

} // namespace duckdb
