#!/bin/sh

SCRIPT=$(realpath "$0")
SCRIPTPATH=$(dirname "$SCRIPT")

echo $SCRIPTPATH

rm -rf	$SCRIPTPATH/.eggs \
		$SCRIPTPATH/.pytest_cache \
		$SCRIPTPATH/build \
		$SCRIPTPATH/duckdb_build \
		$SCRIPTPATH/dist \
		$SCRIPTPATH/vaultdb.egg-info \
		$SCRIPTPATH/duckdb.egg-info \
		$SCRIPTPATH/duckdb.cpp \
		$SCRIPTPATH/duckdb.hpp \
		$SCRIPTPATH/parquet_extension.cpp \
		$SCRIPTPATH/parquet_extension.hpp \
		$SCRIPTPATH/duckdb_tarball
		$SCRIPTPATH/vaultdb_tarball

rm -f	$SCRIPTPATH/sources.list \
		$SCRIPTPATH/includes.list \
		$SCRIPTPATH/githash.list

python3 -m pip uninstall duckdb --yes
python3 -m pip uninstall vaultdb --yes
