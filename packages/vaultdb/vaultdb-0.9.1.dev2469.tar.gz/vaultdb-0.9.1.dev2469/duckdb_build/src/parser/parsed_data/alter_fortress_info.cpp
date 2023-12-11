#include "duckdb/parser/parsed_data/alter_fortress_info.hpp"
#include "duckdb/parser/tableref/basetableref.hpp"

namespace duckdb {

//===--------------------------------------------------------------------===//
// AlterFortressInfo
//===--------------------------------------------------------------------===//
AlterFortressInfo::AlterFortressInfo(AlterFortressType type): AlterInfo(AlterType::ALTER_FORTRESS){
}

AlterFortressInfo::AlterFortressInfo(AlterFortressType type, AlterEntryData data)
    : AlterInfo(AlterType::ALTER_FORTRESS, std::move(data.catalog), std::move(data.schema), std::move(data.name),
                data.if_not_found),
      alter_fortress_type(type) {
}

AlterFortressInfo::~AlterFortressInfo() {
}

CatalogType AlterFortressInfo::GetCatalogType() const {
	return CatalogType::FORTRESS_ENTRY;
}

//===--------------------------------------------------------------------===//
// Modify Fortress
//===--------------------------------------------------------------------===//
ModifyFortressInfo::ModifyFortressInfo(): AlterFortressInfo(AlterFortressType::FORTRESS_CHANGE){
}

ModifyFortressInfo::ModifyFortressInfo(AlterEntryData data)
    : AlterFortressInfo(AlterFortressType::FORTRESS_CHANGE, std::move(data)) {
}
ModifyFortressInfo::~ModifyFortressInfo() {
}

unique_ptr<AlterInfo> ModifyFortressInfo::Copy() const {
	AlterEntryData data(catalog, schema, name, if_not_found);
	auto result = make_uniq<ModifyFortressInfo>(std::move(data));
	result->table = table->Copy();
	result->expression = expression->Copy();
	result->complement_expression = complement_expression->Copy();
	return result;
}

//===--------------------------------------------------------------------===//
// Lock Fortress
//===--------------------------------------------------------------------===//
LockFortressInfo::LockFortressInfo(): AlterFortressInfo(AlterFortressType::LOCK_CHANGE){
}

LockFortressInfo::LockFortressInfo(AlterEntryData data, string start_date, string end_date)
    : AlterFortressInfo(AlterFortressType::LOCK_CHANGE, std::move(data)), start_date(std::move(start_date)), end_date(std::move(end_date)) {
}
LockFortressInfo::~LockFortressInfo() {
}

unique_ptr<AlterInfo> LockFortressInfo::Copy() const {
	AlterEntryData data(catalog, schema, name, if_not_found);
	return make_uniq_base<AlterInfo, LockFortressInfo>(std::move(data), start_date, end_date);
}

//===--------------------------------------------------------------------===//
// Unlock Fortress
//===--------------------------------------------------------------------===//
UnlockFortressInfo::UnlockFortressInfo(): AlterFortressInfo(AlterFortressType::UNLOCK_CHANGE){
}

UnlockFortressInfo::UnlockFortressInfo(AlterEntryData data)
    : AlterFortressInfo(AlterFortressType::UNLOCK_CHANGE, std::move(data)), for_role(string()) {
}
UnlockFortressInfo::~UnlockFortressInfo() {
}

unique_ptr<AlterInfo> UnlockFortressInfo::Copy() const {
	AlterEntryData data(catalog, schema, name, if_not_found);
	auto result = make_uniq<UnlockFortressInfo>(std::move(data));
	result->for_role = for_role;
	return result;
}

} // namespace duckdb

