//===----------------------------------------------------------------------===//
//                         DuckDB
//
// duckdb/parser/parsed_data/alter_fortress_info.hpp
//
//
//===----------------------------------------------------------------------===//

#pragma once

#include "duckdb/common/limits.hpp"
#include "duckdb/common/enums/catalog_type.hpp"
#include "duckdb/parser/parsed_data/create_role_info.hpp"
#include "duckdb/parser/parsed_data/alter_table_info.hpp"
#include "duckdb/parser/tableref.hpp"

namespace duckdb {

//===--------------------------------------------------------------------===//
// Alter Fortress
//===--------------------------------------------------------------------===//
enum class AlterFortressType : uint8_t {
	INVALID = 0,
	FORTRESS_CHANGE = 1,
	LOCK_CHANGE = 2,
	UNLOCK_CHANGE = 3,
};

struct AlterFortressInfo : public AlterInfo {
	AlterFortressInfo(AlterFortressType type, AlterEntryData data);
	~AlterFortressInfo() override;

	AlterFortressType alter_fortress_type;

public:
	CatalogType GetCatalogType() const override;

	void Serialize(Serializer &serializer) const override;
	static unique_ptr<AlterFortressInfo> Deserialize(Deserializer &deserializer);
	
protected:
	AlterFortressInfo(AlterFortressType type);
};

//===--------------------------------------------------------------------===//
// Modify Fortress
//===--------------------------------------------------------------------===//
struct ModifyFortressInfo : public AlterFortressInfo {
	ModifyFortressInfo(AlterEntryData data);
	~ModifyFortressInfo() override;

	//! The table to create the fortress on
	unique_ptr<TableRef> table;
	//! where clause
	unique_ptr<ParsedExpression> expression;
	unique_ptr<ParsedExpression> complement_expression;

public:
	unique_ptr<AlterInfo> Copy() const override;

	void Serialize(Serializer &serializer) const override;
	static unique_ptr<AlterFortressInfo> Deserialize(Deserializer &deserializer);
	
protected:
	ModifyFortressInfo();
};

//===--------------------------------------------------------------------===//
// Lock Fortress
//===--------------------------------------------------------------------===//
struct LockFortressInfo : public AlterFortressInfo {
	LockFortressInfo(AlterEntryData data, string start_date, string end_date);
	~LockFortressInfo() override;

	//! dates
	string start_date;
	string end_date;

public:
	unique_ptr<AlterInfo> Copy() const override;

	void Serialize(Serializer &serializer) const override;
	static unique_ptr<AlterFortressInfo> Deserialize(Deserializer &deserializer);
	
protected:
	LockFortressInfo();
};

//===--------------------------------------------------------------------===//
// Unlock Fortress
//===--------------------------------------------------------------------===//
struct UnlockFortressInfo : public AlterFortressInfo {
	UnlockFortressInfo(AlterEntryData data);
	~UnlockFortressInfo() override;
	//! role privileges
	string for_role;

public:
	unique_ptr<AlterInfo> Copy() const override;

	void Serialize(Serializer &serializer) const override;
	static unique_ptr<AlterFortressInfo> Deserialize(Deserializer &deserializer);
	
protected:
	UnlockFortressInfo();
};
} // namespace duckdb

