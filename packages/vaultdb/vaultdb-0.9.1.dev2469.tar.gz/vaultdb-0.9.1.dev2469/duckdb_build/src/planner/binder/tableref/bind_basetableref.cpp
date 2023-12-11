#include "duckdb/catalog/catalog_entry/table_catalog_entry.hpp"
#include "duckdb/catalog/catalog_entry/table_function_catalog_entry.hpp"
#include "duckdb/catalog/catalog_entry/view_catalog_entry.hpp"
#include "duckdb/common/string_util.hpp"
#include "duckdb/function/table/table_scan.hpp"
#include "duckdb/main/authorizer.hpp"
#include "duckdb/main/client_context.hpp"
#include "duckdb/main/config.hpp"
#include "duckdb/parser/constraints/unique_constraint.hpp"
#include "duckdb/parser/query_node/select_node.hpp"
#include "duckdb/parser/statement/select_statement.hpp"
#include "duckdb/parser/tableref/basetableref.hpp"
#include "duckdb/parser/tableref/subqueryref.hpp"
#include "duckdb/parser/tableref/table_function_ref.hpp"
#include "duckdb/planner/binder.hpp"
#include "duckdb/planner/operator/logical_get.hpp"
#include "duckdb/planner/operator/logical_merge.hpp"
#include "duckdb/planner/tableref/bound_basetableref.hpp"
#include "duckdb/planner/tableref/bound_cteref.hpp"
#include "duckdb/main/extension_helper.hpp"
#include "duckdb/planner/tableref/bound_dummytableref.hpp"
#include "duckdb/planner/tableref/bound_subqueryref.hpp"

namespace duckdb {

static bool TryLoadExtensionForReplacementScan(ClientContext &context, const string &table_name) {
	auto lower_name = StringUtil::Lower(table_name);
	auto &dbconfig = DBConfig::GetConfig(context);

	if (!dbconfig.options.autoload_known_extensions) {
		return false;
	}

	for (const auto &entry : EXTENSION_FILE_POSTFIXES) {
		if (StringUtil::EndsWith(lower_name, entry.name)) {
			ExtensionHelper::AutoLoadExtension(context, entry.extension);
			return true;
		}
	}

	for (const auto &entry : EXTENSION_FILE_CONTAINS) {
		if (StringUtil::Contains(lower_name, entry.name)) {
			ExtensionHelper::AutoLoadExtension(context, entry.extension);
			return true;
		}
	}

	return false;
}

unique_ptr<BoundTableRef> Binder::BindWithReplacementScan(ClientContext &context, const string &table_name,
                                                          BaseTableRef &ref) {
	auto &config = DBConfig::GetConfig(context);
	if (context.config.use_replacement_scans) {
		for (auto &scan : config.replacement_scans) {
			auto replacement_function = scan.function(context, table_name, scan.data.get());
			if (replacement_function) {
				if (!ref.alias.empty()) {
					// user-provided alias overrides the default alias
					replacement_function->alias = ref.alias;
				} else if (replacement_function->alias.empty()) {
					// if the replacement scan itself did not provide an alias we use the table name
					replacement_function->alias = ref.table_name;
				}
				if (replacement_function->type == TableReferenceType::TABLE_FUNCTION) {
					auto &table_function = replacement_function->Cast<TableFunctionRef>();
					table_function.column_name_alias = ref.column_name_alias;
				} else if (replacement_function->type == TableReferenceType::SUBQUERY) {
					auto &subquery = replacement_function->Cast<SubqueryRef>();
					subquery.column_name_alias = ref.column_name_alias;
				} else {
					throw InternalException("Replacement scan should return either a table function or a subquery");
				}
				return Bind(*replacement_function);
			}
		}
	}

	return nullptr;
}

static TableFunction GetParquetScanFunction(TableCatalogEntry &table, ClientContext &context, unique_ptr<FunctionData> &bind_data,
                                                     vector<LogicalType> &return_types, vector<string> &return_names) {
	auto &fs = FileSystem::GetFileSystem(context);
	auto file_path = table.GetRemotePath(context);
	for (auto &col_name : table.partition_key_columns) {
		D_ASSERT(!col_name.empty());
		file_path = fs.JoinPath(file_path, "*");
	}
	file_path = fs.JoinPath(file_path, "*.parquet");

	// TODO: get pattern based on partition key
	vector<Value> parameters;
	parameters.push_back(file_path);

	// fetch the function from the catalog
	QueryErrorContext error_context(nullptr, 0);
	auto func_entry = Catalog::GetEntry(context, CatalogType::TABLE_FUNCTION_ENTRY, INVALID_CATALOG, INVALID_SCHEMA,
	                                    "parquet_scan", OnEntryNotFound::THROW_EXCEPTION, error_context);

	auto &functionentry = func_entry->Cast<TableFunctionCatalogEntry>();

	auto parquet_function = functionentry.functions.GetFunctionByOffset(0);

	named_parameter_map_t named_parameters;
	named_parameters["union_by_name"] = Value::BOOLEAN(true);
	named_parameters["hive_partitioning"] = Value::BOOLEAN(true);
	vector<LogicalType> input_table_types;
	vector<string> input_table_names;
	vector<string> column_name_alias;
	TableFunctionBindInput bind_input(parameters, named_parameters, input_table_types, input_table_names,
	                                  parquet_function.function_info.get());
	try {
		bind_data = parquet_function.bind(context, bind_input, return_types, return_names);
	} catch (const IOException &ex) {
	}

	return parquet_function;
}

unique_ptr<BoundTableRef> Binder::Bind(BaseTableRef &ref) {
	QueryErrorContext error_context(root_statement, ref.query_location);
	// CTEs and views are also referred to using BaseTableRefs, hence need to distinguish here
	// check if the table name refers to a CTE

	// CTE name should never be qualified (i.e. schema_name should be empty)
	optional_ptr<CommonTableExpressionInfo> found_cte = nullptr;
	if (ref.schema_name.empty()) {
		found_cte = FindCTE(ref.table_name, ref.table_name == alias);
	}

	if (found_cte) {
		// Check if there is a CTE binding in the BindContext
		auto &cte = *found_cte;
		auto ctebinding = bind_context.GetCTEBinding(ref.table_name);
		if (!ctebinding) {
			if (CTEIsAlreadyBound(cte)) {
				throw BinderException(
				    "Circular reference to CTE \"%s\", There are two possible solutions. \n1. use WITH RECURSIVE to "
				    "use recursive CTEs. \n2. If "
				    "you want to use the TABLE name \"%s\" the same as the CTE name, please explicitly add "
				    "\"SCHEMA\" before table name. You can try \"main.%s\" (main is the duckdb default schema)",
				    ref.table_name, ref.table_name, ref.table_name);
			}
			// Move CTE to subquery and bind recursively
			SubqueryRef subquery(unique_ptr_cast<SQLStatement, SelectStatement>(cte.query->Copy()));
			subquery.alias = ref.alias.empty() ? ref.table_name : ref.alias;
			subquery.column_name_alias = cte.aliases;
			for (idx_t i = 0; i < ref.column_name_alias.size(); i++) {
				if (i < subquery.column_name_alias.size()) {
					subquery.column_name_alias[i] = ref.column_name_alias[i];
				} else {
					subquery.column_name_alias.push_back(ref.column_name_alias[i]);
				}
			}
			return Bind(subquery, found_cte);
		} else {
			// There is a CTE binding in the BindContext.
			// This can only be the case if there is a recursive CTE,
			// or a materialized CTE present.
			auto index = GenerateTableIndex();
			auto materialized = cte.materialized;
			if (materialized == CTEMaterialize::CTE_MATERIALIZE_DEFAULT) {
#ifdef DUCKDB_ALTERNATIVE_VERIFY
				materialized = CTEMaterialize::CTE_MATERIALIZE_ALWAYS;
#else
				materialized = CTEMaterialize::CTE_MATERIALIZE_NEVER;
#endif
			}
			auto result = make_uniq<BoundCTERef>(index, ctebinding->index, materialized);
			auto b = ctebinding;
			auto alias = ref.alias.empty() ? ref.table_name : ref.alias;
			auto names = BindContext::AliasColumnNames(alias, b->names, ref.column_name_alias);

			bind_context.AddGenericBinding(index, alias, names, b->types);
			// Update references to CTE
			auto cteref = bind_context.cte_references[ref.table_name];
			(*cteref)++;

			result->types = b->types;
			result->bound_columns = std::move(names);
			return std::move(result);
		}
	}
	// not a CTE
	// extract a table or view from the catalog
	BindSchemaOrCatalog(ref.catalog_name, ref.schema_name);
	auto table_or_view = Catalog::GetEntry(context, CatalogType::TABLE_ENTRY, ref.catalog_name, ref.schema_name,
	                                       ref.table_name, OnEntryNotFound::RETURN_NULL, error_context);
	// we still didn't find the table
	if (GetBindingMode() == BindingMode::EXTRACT_NAMES) {
		if (!table_or_view || table_or_view->type == CatalogType::TABLE_ENTRY) {
			// if we are in EXTRACT_NAMES, we create a dummy table ref
			AddTableName(ref.table_name);

			// add a bind context entry
			auto table_index = GenerateTableIndex();
			auto alias = ref.alias.empty() ? ref.table_name : ref.alias;
			vector<LogicalType> types {LogicalType::INTEGER};
			vector<string> names {"__dummy_col" + to_string(table_index)};
			bind_context.AddGenericBinding(table_index, alias, names, types);
			return make_uniq_base<BoundTableRef, BoundEmptyTableRef>(table_index);
		}
	}
	if (!table_or_view) {
		string table_name = ref.catalog_name;
		if (!ref.schema_name.empty()) {
			table_name += (!table_name.empty() ? "." : "") + ref.schema_name;
		}
		table_name += (!table_name.empty() ? "." : "") + ref.table_name;
		// table could not be found: try to bind a replacement scan
		// Try replacement scan bind
		auto replacement_scan_bind_result = BindWithReplacementScan(context, table_name, ref);
		if (replacement_scan_bind_result) {
			return replacement_scan_bind_result;
		}

		// Try autoloading an extension, then retry the replacement scan bind
		auto extension_loaded = TryLoadExtensionForReplacementScan(context, table_name);
		if (extension_loaded) {
			replacement_scan_bind_result = BindWithReplacementScan(context, table_name, ref);
			if (replacement_scan_bind_result) {
				return replacement_scan_bind_result;
				}
			}

		// could not find an alternative: bind again to get the error
		table_or_view = Catalog::GetEntry(context, CatalogType::TABLE_ENTRY, ref.catalog_name, ref.schema_name,
		                                  ref.table_name, OnEntryNotFound::THROW_EXCEPTION, error_context);
	}
	switch (table_or_view->type) {
	case CatalogType::TABLE_ENTRY: {
		// Authorize role
		if (root_statement) {
			context.authorizer->Authorize_table(ref.schema_name, ref.table_name, root_statement->type);
		}
		// base table: create the BoundBaseTableRef node
		auto table_index = GenerateTableIndex();
		auto &table = table_or_view->Cast<TableCatalogEntry>();

		unique_ptr<FunctionData> bind_data;
		auto scan_function = table.GetScanFunction(context, bind_data);
		auto alias = ref.alias.empty() ? ref.table_name : ref.alias;
		// TODO: bundle the type and name vector in a struct (e.g PackedColumnMetadata)
		vector<LogicalType> table_types;
		vector<string> table_names;
		vector<TableColumnType> table_categories;

		vector<LogicalType> return_types;
		vector<string> return_names;
		for (auto &col : table.GetColumns().Logical()) {
			table_types.push_back(col.Type());
			table_names.push_back(col.Name());
			return_types.push_back(col.Type());
			return_names.push_back(col.Name());
		}
		table_names = BindContext::AliasColumnNames(alias, table_names, ref.column_name_alias);

		if (root_statement && root_statement->merge_remote) {
			//! VaultDB: Merge Data if merge is enabled. Else statement was original only if added here
			unique_ptr<FunctionData> parquet_bind_data;
			auto parquet_function = GetParquetScanFunction(table, context, parquet_bind_data, return_types, return_names);
			// VaultDB: there is not need to inherit if Files are not there
			if (parquet_bind_data) {
				auto logical_get = make_uniq<LogicalMerge>(table_index, scan_function, std::move(bind_data),
				                                           parquet_function, std::move(parquet_bind_data),
				                                           std::move(return_types), std::move(return_names));

				for (auto column_index : table.GetPrimaryKeyColumnIndex()) {
					logical_get->merge_column_indexes.push_back(column_index);
				}

				bind_context.AddBaseTable(table_index, alias, table_names, table_types, logical_get->column_ids,
				                          logical_get->GetTable().get());

				return make_uniq_base<BoundTableRef, BoundBaseTableRef>(table, std::move(logical_get));
			}
		}
		auto logical_get = make_uniq<LogicalGet>(table_index, scan_function, std::move(bind_data),
		                                         std::move(return_types), std::move(return_names));
		bind_context.AddBaseTable(table_index, alias, table_names, table_types, logical_get->column_ids,
		                          logical_get->GetTable().get());

		return make_uniq_base<BoundTableRef, BoundBaseTableRef>(table, std::move(logical_get));
	}
	case CatalogType::VIEW_ENTRY: {
		// the node is a view: get the query that the view represents
		auto &view_catalog_entry = table_or_view->Cast<ViewCatalogEntry>();
		// Authorize role
		if (root_statement)
			context.authorizer->Authorize_view(view_catalog_entry.schema.name, view_catalog_entry.name,
			                                   root_statement->type);
		// We need to use a new binder for the view that doesn't reference any CTEs
		// defined for this binder so there are no collisions between the CTEs defined
		// for the view and for the current query
		bool inherit_ctes = false;
		auto view_binder = Binder::CreateBinder(context, this, inherit_ctes);
		view_binder->can_contain_nulls = true;
		SubqueryRef subquery(unique_ptr_cast<SQLStatement, SelectStatement>(view_catalog_entry.query->Copy()));
		subquery.alias = ref.alias.empty() ? ref.table_name : ref.alias;
		subquery.column_name_alias =
		    BindContext::AliasColumnNames(subquery.alias, view_catalog_entry.aliases, ref.column_name_alias);
		// bind the child subquery
		view_binder->AddBoundView(view_catalog_entry);
		auto bound_child = view_binder->Bind(subquery);
		if (!view_binder->correlated_columns.empty()) {
			throw BinderException("Contents of view were altered - view bound correlated columns");
		}

		D_ASSERT(bound_child->type == TableReferenceType::SUBQUERY);
		// verify that the types and names match up with the expected types and names
		auto &bound_subquery = bound_child->Cast<BoundSubqueryRef>();
		if (GetBindingMode() != BindingMode::EXTRACT_NAMES &&
		    bound_subquery.subquery->types != view_catalog_entry.types) {
			throw BinderException("Contents of view were altered: types don't match!");
		}
		bind_context.AddView(bound_subquery.subquery->GetRootIndex(), subquery.alias, subquery,
		                     *bound_subquery.subquery, &view_catalog_entry);
		return bound_child;
	}
	default:
		throw InternalException("Catalog entry type");
	}
}
} // namespace duckdb
