#!/bin/bash
set -e

# shellcheck disable=SC2016
export PGPASSWORD='$POSTGRES_PASSWORD'; psql -v ON_ERROR_STOP=1 --username "$POSTGRES_USER" --dbname "$POSTGRES_DB" <<-EOSQL
	CREATE USER rw_user WITH PASSWORD 'rwPassword';
	CREATE USER ro_user WITH PASSWORD 'roPassword';
	CREATE DATABASE lash OWNER rw_user ENCODING UTF8;
	GRANT ALL PRIVILEGES ON DATABASE lash TO rw_user;
	GRANT CONNECT ON DATABASE lash TO ro_user;
EOSQL

export PGPASSWORD='rwPassword'; psql -v ON_ERROR_STOP=1 --username "rw_user" --dbname "lash" <<-EOSQL
	CREATE SCHEMA lash;
	alter database lash SET search_path TO lash;
	GRANT USAGE ON SCHEMA lash TO ro_user;
	ALTER DEFAULT PRIVILEGES IN SCHEMA lash GRANT SELECT ON TABLES TO ro_user;
EOSQL
