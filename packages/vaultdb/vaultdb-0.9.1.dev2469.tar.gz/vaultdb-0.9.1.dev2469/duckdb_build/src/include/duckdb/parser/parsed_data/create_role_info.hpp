//===----------------------------------------------------------------------===//
//                         DuckDB
//
// duckdb/parser/parsed_data/create_role_info.hpp
//
//
//===----------------------------------------------------------------------===//

#pragma once

#include "duckdb/common/limits.hpp"
#include "duckdb/common/map.hpp"
#include "duckdb/parser/parsed_data/create_info.hpp"

namespace duckdb {

struct CreatePrivilegeInfo : public CreateInfo {
	DUCKDB_API CreatePrivilegeInfo(CatalogType type, string name)
	    : CreateInfo(type, SECURITY_SCHEMA), name(name), privileges(1 << 0), grantOption(false) {
	}

	string name;
	uint64_t privileges;
	bool grantOption;
	vector<string> unauthorized_columns;

public:
	unique_ptr<CreatePrivilegeInfo> CopyPrivilegeInfo() const;
	DUCKDB_API unique_ptr<CreateInfo> Copy() const override {
		return CopyPrivilegeInfo();
	};

	DUCKDB_API void Serialize(Serializer &serializer) const override;
	DUCKDB_API static unique_ptr<CreateInfo> Deserialize(Deserializer &deserializer);
};

struct CreateRoleInfo : public CreateInfo {
	DUCKDB_API CreateRoleInfo()
	    : CreateInfo(CatalogType::ROLE_ENTRY, SECURITY_SCHEMA), name(string()), login(false), superuser(false) {
	}

	//! role name to create
	string name;
	//! role publickey
	string publickey;
	//! can role login
	bool login;
	//! is role super user
	bool superuser;

	//! privileges (maps used to make sure we can find different privileges by type and name)
	map<CatalogType, map<string, unique_ptr<CreatePrivilegeInfo>>> privileges;

public:
	unique_ptr<CreateRoleInfo> CopyRole() const;
	unique_ptr<CreateInfo> Copy() const override {
		return CopyRole();
	};

	DUCKDB_API void Serialize(Serializer &serializer) const override;
	DUCKDB_API static unique_ptr<CreateInfo> Deserialize(Deserializer &deserializer);
};

} // namespace duckdb
