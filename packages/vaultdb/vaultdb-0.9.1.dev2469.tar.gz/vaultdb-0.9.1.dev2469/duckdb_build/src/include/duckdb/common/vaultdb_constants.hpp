//===----------------------------------------------------------------------===//
//                         DuckDB
//
// duckdb/common/vaultdb_constants.hpp
//
//
//===----------------------------------------------------------------------===//

#pragma once

#include "duckdb/common/typedefs.hpp"

#include <atomic>

namespace duckdb {
// NOTE: there is a copy of this in the Postgres' parser grammar (gram.y)
#define DEFAULT_SCHEMA  "main"
#define INVALID_SCHEMA  ""
#define INVALID_CATALOG ""
#define SYSTEM_CATALOG  "system"
#define TEMP_CATALOG    "temp"

#define SECURITY_SCHEMA "security"
#define REMOTE_DATA_PATH "remote_data_config"
#define REMOTE_MERGE_PATH "remote_merge_config"
// Roles for internal Use
#define INTERNAL_ROLE "internal"
#define ADMIN_ROLE    "vaultdb"

// PI TAGS for internal Use
#define PI_TAG  "PI"
#define PII_TAG "PII"

//! REMOTE Parquet data row id. Used to diffrentiate between remote and local data row
extern const row_t REMOTE_ROW_ID;

} // namespace duckdb
