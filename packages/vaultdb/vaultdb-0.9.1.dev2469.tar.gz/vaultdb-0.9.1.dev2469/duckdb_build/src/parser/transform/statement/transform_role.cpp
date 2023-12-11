#include "duckdb/parser/parsed_data/create_role_info.hpp"
#include "duckdb/parser/parsed_data/alter_role_info.hpp"
#include "duckdb/parser/statement/create_statement.hpp"
#include "duckdb/parser/statement/alter_statement.hpp"
#include "duckdb/parser/transformer.hpp"

namespace duckdb {

unique_ptr<CreateStatement> Transformer::TransformCreateRole(duckdb_libpgquery::PGCreateRoleStmt &stmt) {

	context->authorizer->Authorize_schema(SECURITY_SCHEMA, duckdb_libpgquery::PG_PRIVILEGE_CREATE);

	auto result = make_uniq<CreateStatement>();
	auto info = make_uniq<CreateRoleInfo>();
	info->name = stmt.role->relname;
	if (stmt.options & duckdb_libpgquery::PG_ROLEOPT_NOLOGIN)
		info->login = false;
	else if (stmt.options & duckdb_libpgquery::PG_ROLEOPT_LOGIN)
		info->login = true;
	else
		info->login = true;

	if (stmt.options & duckdb_libpgquery::PG_ROLEOPT_SUPERUSER) {
		if (!context->authorizer->GetCurrentRole()->superuser)
			throw PermissionException("Only Super User can create super user.");
		info->superuser = true;
	} else if (stmt.options & duckdb_libpgquery::PG_ROLEOPT_NOSUPERUSER)
		info->superuser = false;
	else
		info->superuser = false;

	result->info = std::move(info);
	return result;
}

unique_ptr<AlterStatement> Transformer::TransformAlterRole(duckdb_libpgquery::PGAlterRoleStmt &stmt) {
	context->authorizer->Authorize_schema(SECURITY_SCHEMA, duckdb_libpgquery::PG_PRIVILEGE_ALTER);

	auto result = make_uniq<AlterStatement>();
	AlterEntryData data(INVALID_CATALOG, SECURITY_SCHEMA, stmt.role->relname, OnEntryNotFound::RETURN_NULL);
	if (stmt.options & duckdb_libpgquery::PG_ROLEOPT_NOLOGIN) {
		auto info = make_uniq<ModifyRoleFlagInfo>(AlterRoleType::LOGIN_CHANGE, std::move(data), false);
		result->info = std::move(info);
		return result;
	} else if (stmt.options & duckdb_libpgquery::PG_ROLEOPT_LOGIN) {
		auto info = make_uniq<ModifyRoleFlagInfo>(AlterRoleType::LOGIN_CHANGE, std::move(data), true);
		result->info = std::move(info);
		return result;
	}

	if (stmt.options & duckdb_libpgquery::PG_ROLEOPT_SUPERUSER) {
		auto info = make_uniq<ModifyRoleFlagInfo>(AlterRoleType::SUPERUSER_CHANGE, std::move(data), true);
		result->info = std::move(info);
		return result;
	} else if (stmt.options & duckdb_libpgquery::PG_ROLEOPT_NOSUPERUSER) {
		auto info = make_uniq<ModifyRoleFlagInfo>(AlterRoleType::SUPERUSER_CHANGE, std::move(data), false);
		result->info = std::move(info);
		return result;
	}

	throw Exception("Failed: Invalid Role Options!");
}

} // namespace duckdb
