#include "duckdb/catalog/catalog_entry/fortress_catalog_entry.hpp"

#include "duckdb/catalog/catalog_entry/schema_catalog_entry.hpp"
#include "duckdb/catalog/catalog_entry/table_catalog_entry.hpp"
#include "duckdb/catalog/dependency_manager.hpp"
#include "duckdb/common/exception.hpp"
#include "duckdb/common/types/date.hpp"
#include "duckdb/common/types/timestamp.hpp"
#include "duckdb/parser/parsed_data/alter_fortress_info.hpp"
#include "duckdb/parser/parsed_data/create_view_info.hpp"
#include "duckdb/parser/tableref/basetableref.hpp"
#include "duckdb/planner/binder.hpp"

#include <algorithm>
#include <sstream>

namespace duckdb {

FortressCatalogEntry::FortressCatalogEntry(Catalog &catalog, SchemaCatalogEntry &schema, CreateFortressInfo &info)
    : StandardEntry(CatalogType::FORTRESS_ENTRY, schema, catalog, info.name), locked(std::move(info.locked)),
      start_date(std::move(info.start_date)), end_date(std::move(info.end_date)),
      unlocked_for_role(std::move(info.unlocked_for_role)), table(std::move(info.table)),
      expression(std::move(info.expression)), complement_expression(std::move(info.complement_expression)) {
}

unique_ptr<CatalogEntry> FortressCatalogEntry::AlterEntry(ClientContext &context, AlterInfo &alterinfo) {
	if (alterinfo.type != AlterType::ALTER_FORTRESS) {
		throw CatalogException("Can only modify fortress with ALTER FORTRESS statement");
	}
	auto &fortress_info = alterinfo.Cast<AlterFortressInfo>();
	auto info = make_uniq<CreateFortressInfo>();
	info->name = alterinfo.name;
	info->table = std::move(table);
	info->expression = std::move(expression);
	info->complement_expression = std::move(complement_expression);
	info->unlocked_for_role = unlocked_for_role;
	info->locked = locked;
	info->start_date = start_date;
	info->end_date = end_date;

	switch (fortress_info.alter_fortress_type) {
	case AlterFortressType::FORTRESS_CHANGE: {
		auto &modify_info = fortress_info.Cast<ModifyFortressInfo>();
		info->table = modify_info.table->Copy();
		info->expression = modify_info.expression->Copy();
		info->complement_expression = modify_info.complement_expression->Copy();
		return make_uniq<FortressCatalogEntry>(catalog, schema, *info);
	}
	case AlterFortressType::LOCK_CHANGE: {
		auto &locked_info = fortress_info.Cast<LockFortressInfo>();
		info->locked = true;
		info->start_date = locked_info.start_date;
		info->end_date = locked_info.end_date;
		if (!unlocked_for_role.empty())
			info->unlocked_for_role = unlocked_for_role;
		return make_uniq<FortressCatalogEntry>(catalog, schema, *info);
	}
	case AlterFortressType::UNLOCK_CHANGE: {
		auto &unlock_info = fortress_info.Cast<UnlockFortressInfo>();
		if (!unlock_info.for_role.empty())
			info->unlocked_for_role = unlock_info.for_role;
		else {
			info->locked = false;
			info->unlocked_for_role = std::move(string());
			info->start_date = std::move(string());
			info->end_date = std::move(string());
		}
		return make_uniq<FortressCatalogEntry>(catalog, schema, *info);
	}
	default:
		throw InternalException("Unrecognized alter table type!");
	}
}

unique_ptr<CreateInfo> FortressCatalogEntry::GetInfo() const {
	auto result = make_uniq<CreateFortressInfo>();
	result->schema = schema.name;
	result->name = name;
	result->table = table->Copy();
	result->expression = expression->Copy();
	result->complement_expression = complement_expression->Copy();
	result->locked = locked;	
	if (locked) {
		result->start_date = start_date;
		result->end_date = end_date;
	}
	
	return std::move(result);
}

string FortressCatalogEntry::ToSQL() const {
	auto basetable = unique_ptr_cast<TableRef, BaseTableRef>(table->Copy());
	std::stringstream ss;
	ss << "CREATE FORTRESS ";
	ss << name;
	ss << " ON ";
	if (!basetable->schema_name.empty()) {
		ss << name;
		ss << basetable->schema_name;
		ss << ".";
	}
	ss << basetable->table_name;
	ss << " ";
	ss << expression->ToString();
	ss << ";";
	return ss.str();
}

bool FortressCatalogEntry::isLocked() {
	if (!locked)
		return false;
	if (!start_date.empty() && !end_date.empty()) {
		auto begin = Date::FromString(start_date);
		auto end = Date::FromString(end_date);
		auto currentdate = Timestamp::GetDate(Timestamp::GetCurrentTimestamp());
		if (currentdate < begin || currentdate >= end)
			return false;
	}
	return true;
}

void FortressCatalogEntry::AddFortressToTableEntry(ClientContext &context) {
	auto basetable = unique_ptr_cast<TableRef, BaseTableRef>(table->Copy());
	auto table_entry = Catalog::GetEntry<TableCatalogEntry>(context, basetable->catalog_name,
						basetable->schema_name, basetable->table_name, OnEntryNotFound::RETURN_NULL);
	if (!table_entry)
		return;															 
	table_entry->fortress.insert(name);
}

} // namespace duckdb
