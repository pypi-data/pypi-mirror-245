#include "duckdb/catalog/catalog_entry/role_catalog_entry.hpp"

#include "duckdb/catalog/catalog_entry/fortress_catalog_entry.hpp"
#include "duckdb/catalog/catalog_entry/schema_catalog_entry.hpp"
#include "duckdb/catalog/catalog_entry/table_catalog_entry.hpp"
#include "duckdb/catalog/dependency_manager.hpp"
#include "duckdb/common/exception.hpp"
#include "duckdb/parser/parsed_data/alter_role_info.hpp"

#include <algorithm>
#include <sstream>

namespace duckdb {

RoleCatalogEntry::RoleCatalogEntry(Catalog &catalog, SchemaCatalogEntry &schema, CreateRoleInfo &info)
    : StandardEntry(CatalogType::ROLE_ENTRY, schema, catalog, info.name), info(std::move(info.CopyRole())) {
}

unique_ptr<CatalogEntry> RoleCatalogEntry::AlterEntry(ClientContext &context, AlterInfo &alterinfo) {
	D_ASSERT(!internal);
	if (alterinfo.type != AlterType::ALTER_ROLE) {
		throw CatalogException("Can only modify role with ALTER ROLE statement");
	}
	auto &role_info = alterinfo.Cast<AlterRoleInfo>();
	switch (role_info.alter_role_type) {
	case AlterRoleType::SUPERUSER_CHANGE:
	case AlterRoleType::LOGIN_CHANGE: {
		auto &roleflag_info = role_info.Cast<ModifyRoleFlagInfo>();
		auto copied_role = info->CopyRole();
		if (role_info.alter_role_type == AlterRoleType::LOGIN_CHANGE)
			copied_role->login = roleflag_info.flag;
		else
			copied_role->superuser = roleflag_info.flag;
		return make_uniq<RoleCatalogEntry>(catalog, schema, *copied_role);
	}
	case AlterRoleType::REVOKE_PRIVILEGES:
	case AlterRoleType::GRANT_PRIVILEGES: {
		auto &roleflag_info = role_info.Cast<ModifyRolePrivilegeInfo>();
		auto copied_role = info->CopyRole();
		if (copied_role->superuser) {
			throw CatalogException("This is a super user role and has access to everything. Please modify that using "
			                       "alter role to restrict access.");
		}

		unique_ptr<CreatePrivilegeInfo> privilege;
		auto &privilegetype = copied_role->privileges[roleflag_info.resourcetype];
		if (!privilegetype.empty())
			privilege = std::move(privilegetype[roleflag_info.resourcename]);
		if (!privilege)
			privilege = make_uniq<CreatePrivilegeInfo>(roleflag_info.resourcetype, roleflag_info.resourcename);

		switch (roleflag_info.resourcetype) {
		case CatalogType::TABLE_ENTRY: {
			for (idx_t i = 0; i < roleflag_info.aliases.size(); i++) {
				auto idx = std::find(privilege->unauthorized_columns.begin(), privilege->unauthorized_columns.end(),
				                     roleflag_info.aliases[i]);
				if (role_info.alter_role_type == AlterRoleType::REVOKE_PRIVILEGES &&
				    (privilege->unauthorized_columns.empty() || idx == privilege->unauthorized_columns.end())) {
					privilege->unauthorized_columns.emplace_back(roleflag_info.aliases[i]);
				} else if (idx != privilege->unauthorized_columns.end()) {
					privilege->unauthorized_columns.erase(idx);
				}
			}
			break;
		}
		case CatalogType::FORTRESS_ENTRY:
		case CatalogType::TAG_ENTRY:
		case CatalogType::CONFIG_ENTRY:
		case CatalogType::VIEW_ENTRY:
		case CatalogType::SCHEMA_ENTRY:
			break;
		default:
			throw InternalException("Unrecognized resource type %s !", CatalogTypeToString(roleflag_info.resourcetype));
		}

		if (roleflag_info.modifygrantOption)
			privilege->grantOption = !privilege->grantOption;
		if (role_info.alter_role_type == AlterRoleType::REVOKE_PRIVILEGES) {
			if (roleflag_info.privileges > 1 && (privilege->privileges & roleflag_info.privileges))
				privilege->privileges &= ~roleflag_info.privileges;
		} else {
			if (!(privilege->privileges & roleflag_info.privileges))
				privilege->privileges |= roleflag_info.privileges;
			if (privilege->privileges == 1)
				privilege->privileges |= roleflag_info.privileges;
		}
		copied_role->privileges[roleflag_info.resourcetype][roleflag_info.resourcename] = std::move(privilege);
		return make_uniq<RoleCatalogEntry>(catalog, schema, *copied_role);
	}
	default:
		throw InternalException("Unrecognized alter view type!");
	}
}

unique_ptr<CreateInfo> RoleCatalogEntry::GetInfo() const {
	auto result = make_uniq<CreateRoleInfo>();
	result->schema = schema.name;
	result->name = name;
	result->login = info->login;
	result->superuser = info->superuser;
	for (auto &privilegetypes : info->privileges) {
		for (auto &privilege : privilegetypes.second) {
			result->privileges[privilegetypes.first][privilege.second->name] = privilege.second->CopyPrivilegeInfo();
		}
	}
	
	return std::move(result);
}

string RoleCatalogEntry::ToSQL() const {
	std::stringstream ss;
	ss << "CREATE ROLE ";
	ss << name;
	ss << ";";
	return ss.str();
}

} // namespace duckdb
