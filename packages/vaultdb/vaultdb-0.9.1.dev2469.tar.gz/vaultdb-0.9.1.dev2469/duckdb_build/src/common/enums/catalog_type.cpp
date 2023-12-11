#include "duckdb/common/enums/catalog_type.hpp"
#include "duckdb/common/string_util.hpp"
#include "duckdb/common/exception.hpp"

namespace duckdb {

// LCOV_EXCL_START
string CatalogTypeToString(CatalogType type) {
	switch (type) {
	case CatalogType::COLLATION_ENTRY:
		return "Collation";
	case CatalogType::TYPE_ENTRY:
		return "Type";
	case CatalogType::TABLE_ENTRY:
		return "Table";
	case CatalogType::SCHEMA_ENTRY:
		return "Schema";
	case CatalogType::DATABASE_ENTRY:
		return "Database";
	case CatalogType::TABLE_FUNCTION_ENTRY:
		return "Table Function";
	case CatalogType::SCALAR_FUNCTION_ENTRY:
		return "Scalar Function";
	case CatalogType::AGGREGATE_FUNCTION_ENTRY:
		return "Aggregate Function";
	case CatalogType::COPY_FUNCTION_ENTRY:
		return "Copy Function";
	case CatalogType::PRAGMA_FUNCTION_ENTRY:
		return "Pragma Function";
	case CatalogType::MACRO_ENTRY:
		return "Macro Function";
	case CatalogType::TABLE_MACRO_ENTRY:
		return "Table Macro Function";
	case CatalogType::VIEW_ENTRY:
		return "View";
	case CatalogType::INDEX_ENTRY:
		return "Index";
	case CatalogType::PREPARED_STATEMENT:
		return "Prepared Statement";
	case CatalogType::SEQUENCE_ENTRY:
		return "Sequence";
	case CatalogType::ROLE_ENTRY:
		return "Role";
	case CatalogType::TAG_ENTRY:
		return "Tag";
	case CatalogType::CONFIG_ENTRY:
		return "Config";
	case CatalogType::FORTRESS_ENTRY:
		return "Fortress";
	case CatalogType::INVALID:
	case CatalogType::DELETED_ENTRY:
	case CatalogType::UPDATED_ENTRY:
		break;
	}
	return "INVALID";
}
// LCOV_EXCL_STOP

// LCOV_EXCL_START
CatalogType StringToCatalogType(const string &type) {
	string lower_case_type  = StringUtil::Lower(type);
	StringUtil::Trim(lower_case_type);
	if (lower_case_type == "collation")
		return CatalogType::COLLATION_ENTRY;
	if (lower_case_type == "type")
		return CatalogType::TYPE_ENTRY;
	if (lower_case_type == "table")
		return CatalogType::TABLE_ENTRY;
	if (lower_case_type == "schema")
		return CatalogType::SCHEMA_ENTRY;
	if (lower_case_type == "table function")
		return CatalogType::TABLE_FUNCTION_ENTRY;
	if (lower_case_type == "scalar function")
		return CatalogType::SCALAR_FUNCTION_ENTRY;
	if (lower_case_type == "aggregate function")
		return CatalogType::AGGREGATE_FUNCTION_ENTRY;
	if (lower_case_type == "copy function")
		return CatalogType::COPY_FUNCTION_ENTRY;
	if (lower_case_type == "pragma function")
		return CatalogType::PRAGMA_FUNCTION_ENTRY;
	if (lower_case_type == "macro function")
		return CatalogType::MACRO_ENTRY;
	if (lower_case_type == "view")
		return CatalogType::VIEW_ENTRY;
	if (lower_case_type == "index")
		return CatalogType::INDEX_ENTRY;
	if (lower_case_type == "prepared statement")
		return CatalogType::PREPARED_STATEMENT;
	if (lower_case_type == "sequence")
		return CatalogType::SEQUENCE_ENTRY;
	if (lower_case_type == "role")
		return CatalogType::ROLE_ENTRY;
	if (lower_case_type == "tag")
		return CatalogType::TAG_ENTRY;
	if (lower_case_type == "config")
		return CatalogType::CONFIG_ENTRY;

	return CatalogType::INVALID;
}

} // namespace duckdb
