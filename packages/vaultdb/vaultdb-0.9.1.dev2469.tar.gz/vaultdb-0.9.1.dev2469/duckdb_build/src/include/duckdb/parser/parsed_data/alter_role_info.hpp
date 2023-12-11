//===----------------------------------------------------------------------===//
//                         DuckDB
//
// duckdb/parser/parsed_data/alter_role_info.hpp
//
//
//===----------------------------------------------------------------------===//

#pragma once

#include "duckdb/common/limits.hpp"
#include "duckdb/common/enums/catalog_type.hpp"
#include "duckdb/parser/parsed_data/create_role_info.hpp"
#include "duckdb/parser/parsed_data/alter_table_info.hpp"

namespace duckdb {

//===--------------------------------------------------------------------===//
// Alter Role
//===--------------------------------------------------------------------===//
enum class AlterRoleType : uint8_t {
	INVALID = 0,
	LOGIN_CHANGE = 1,
	SUPERUSER_CHANGE = 2,
	GRANT_PRIVILEGES = 3,
	REVOKE_PRIVILEGES = 4,
};

struct AlterRoleInfo : public AlterInfo {
	AlterRoleInfo(AlterRoleType type, AlterEntryData data);
	~AlterRoleInfo() override;

	AlterRoleType alter_role_type;

public:
	CatalogType GetCatalogType() const override;

	void Serialize(Serializer &serializer) const override;
	static unique_ptr<AlterRoleInfo> Deserialize(Deserializer &deserializer);
	
protected:
	AlterRoleInfo(AlterRoleType type);
};

//===--------------------------------------------------------------------===//
// Modify Role
//===--------------------------------------------------------------------===//
struct ModifyRoleFlagInfo : public AlterRoleInfo {
	ModifyRoleFlagInfo(AlterRoleType type, AlterEntryData data, bool flag);
	~ModifyRoleFlagInfo() override;

	//! modified role flag
	bool flag;

public:
	unique_ptr<AlterInfo> Copy() const override;

	void Serialize(Serializer &serializer) const override;
	static unique_ptr<AlterRoleInfo> Deserialize(Deserializer &deserializer, AlterRoleType alter_role_type);

protected:
	ModifyRoleFlagInfo(AlterRoleType type);
};

//===--------------------------------------------------------------------===//
// Modify Role Privileges
//===--------------------------------------------------------------------===//
struct ModifyRolePrivilegeInfo : public AlterRoleInfo {
	ModifyRolePrivilegeInfo(AlterRoleType type, AlterEntryData data, CatalogType resourcetype, string resourcename, uint64_t privileges, bool modifygrantOption);
	~ModifyRolePrivilegeInfo() override;

	//! modified role privileges
	CatalogType resourcetype;
	string resourcename;
	vector<string> aliases;
	uint64_t privileges;
	bool modifygrantOption;

public:
	unique_ptr<AlterInfo> Copy() const override;
	
	void Serialize(Serializer &serializer) const override;
	static unique_ptr<AlterRoleInfo> Deserialize(Deserializer &deserializer, AlterRoleType alter_role_type);

protected:
	ModifyRolePrivilegeInfo(AlterRoleType type);
};
} // namespace duckdb

