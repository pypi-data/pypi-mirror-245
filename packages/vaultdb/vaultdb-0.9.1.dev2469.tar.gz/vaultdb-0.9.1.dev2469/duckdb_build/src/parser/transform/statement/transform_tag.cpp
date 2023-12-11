#include "duckdb/parser/parsed_data/create_tag_info.hpp"
#include "duckdb/parser/statement/create_statement.hpp"
#include "duckdb/parser/statement/drop_statement.hpp"
#include "duckdb/parser/transformer.hpp"

namespace duckdb {

unique_ptr<CreateStatement> Transformer::TransformCreateTag(duckdb_libpgquery::PGCreateTagStmt &stmt) {
	context->authorizer->Authorize_schema(SECURITY_SCHEMA, duckdb_libpgquery::PG_PRIVILEGE_CREATE);

	auto result = make_uniq<CreateStatement>();
	auto info = make_uniq<CreateTagInfo>();
	info->name = stmt.tag->relname;
	if (stmt.comment) {
		auto val = (duckdb_libpgquery::PGValue *)stmt.comment;
		info->comment = val->val.str;
	} else
		info->comment = info->name;

	if (stmt.function) {
		auto expression = TransformExpression(stmt.function);
		info->function = std::move(expression);
	}
	result->info = std::move(info);
	return result;
}

} // namespace duckdb
