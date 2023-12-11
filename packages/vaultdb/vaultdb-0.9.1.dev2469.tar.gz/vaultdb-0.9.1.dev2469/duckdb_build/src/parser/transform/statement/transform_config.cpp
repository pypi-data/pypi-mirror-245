#include "duckdb/parser/parsed_data/create_config_info.hpp"
#include "duckdb/parser/statement/create_statement.hpp"
#include "duckdb/parser/statement/drop_statement.hpp"
#include "duckdb/parser/transformer.hpp"

namespace duckdb {

unique_ptr<CreateStatement> Transformer::TransformCreateConfig(duckdb_libpgquery::PGCreateConfigStmt &stmt) {
	context->authorizer->Authorize_schema(SECURITY_SCHEMA, duckdb_libpgquery::PG_PRIVILEGE_CREATE);

	auto result = make_uniq<CreateStatement>();
	auto info = make_uniq<CreateConfigInfo>();
	info->on_conflict = TransformOnConflict(stmt.onconflict);
	if (stmt.options & duckdb_libpgquery::PG_CONFIGOPT_DATA_PATH) {
		info->name = REMOTE_DATA_PATH;
		info->value = stmt.config->relname;
	} else {
		info->name = REMOTE_MERGE_PATH;
		info->value = stmt.config->relname;
	}

	result->info = std::move(info);
	return result;
}

} // namespace duckdb
