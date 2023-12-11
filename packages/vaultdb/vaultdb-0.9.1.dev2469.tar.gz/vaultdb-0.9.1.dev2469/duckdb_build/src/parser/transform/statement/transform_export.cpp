#include "duckdb/parser/statement/export_statement.hpp"
#include "duckdb/parser/transformer.hpp"

namespace duckdb {

unique_ptr<ExportStatement> Transformer::TransformExport(duckdb_libpgquery::PGExportStmt &stmt) {
	auto info = make_uniq<CopyInfo>();
	info->push_to_remote = stmt.push_to_remote;
	if (!info->push_to_remote){
		info->file_path = stmt.filename;
		info->format = "csv";
	} 
	else {
		info->merge_to_remote = stmt.merge_to_remote;
		info->file_path = string();
		info->format = "parquet";
	}
	info->is_from = false;
	// handle export options
	TransformCopyOptions(*info, stmt.options);

	auto result = make_uniq<ExportStatement>(std::move(info));
	if (stmt.database) {
		result->database = stmt.database;
	}
	return result;
}

} // namespace duckdb
