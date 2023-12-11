#include "duckdb/parser/parsed_data/alter_role_info.hpp"

namespace duckdb {

//===--------------------------------------------------------------------===//
// AlterRoleInfo
//===--------------------------------------------------------------------===//
AlterRoleInfo::AlterRoleInfo(AlterRoleType type) : AlterInfo(AlterType::ALTER_ROLE), alter_role_type(type) {
}

AlterRoleInfo::AlterRoleInfo(AlterRoleType type, AlterEntryData data)
    : AlterInfo(AlterType::ALTER_ROLE, std::move(data.catalog), std::move(data.schema), std::move(data.name),
                data.if_not_found),
      alter_role_type(type) {
}
AlterRoleInfo::~AlterRoleInfo() {
}

CatalogType AlterRoleInfo::GetCatalogType() const {
	return CatalogType::ROLE_ENTRY;
}

//===--------------------------------------------------------------------===//
// Modify Login flag
//===--------------------------------------------------------------------===//
ModifyRoleFlagInfo::ModifyRoleFlagInfo(AlterRoleType type): AlterRoleInfo(type) {
}

ModifyRoleFlagInfo::ModifyRoleFlagInfo(AlterRoleType type, AlterEntryData data, bool flag)
    : AlterRoleInfo(type, std::move(data)), flag(std::move(flag)) {
}
ModifyRoleFlagInfo::~ModifyRoleFlagInfo() {
}

unique_ptr<AlterInfo> ModifyRoleFlagInfo::Copy() const {
	AlterEntryData data(catalog, schema, name, if_not_found);
	return make_uniq_base<AlterInfo, ModifyRoleFlagInfo>(alter_role_type, std::move(data), flag);
}

//===--------------------------------------------------------------------===//
// Modify Role Privileges
//===--------------------------------------------------------------------===//
ModifyRolePrivilegeInfo::ModifyRolePrivilegeInfo(AlterRoleType type): AlterRoleInfo(type) {
}

ModifyRolePrivilegeInfo::ModifyRolePrivilegeInfo(AlterRoleType type, AlterEntryData data, CatalogType resourcetype, string resourcename, uint64_t privileges, bool modifygrantOption)
    : AlterRoleInfo(type, std::move(data)), resourcetype(std::move(resourcetype)), resourcename(std::move(resourcename)), privileges(privileges), modifygrantOption(std::move(modifygrantOption)) {
}
ModifyRolePrivilegeInfo::~ModifyRolePrivilegeInfo() {
}

unique_ptr<AlterInfo> ModifyRolePrivilegeInfo::Copy() const {
	AlterEntryData data(catalog, schema, name, if_not_found);
	return make_uniq_base<AlterInfo, ModifyRolePrivilegeInfo>(alter_role_type, std::move(data), resourcetype,
	                                                          resourcename, privileges, modifygrantOption);
}

} // namespace duckdb

