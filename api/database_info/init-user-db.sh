#!/bin/bash
set -e
chown -R 999:999 ./db/data/pgdata
psql -v ON_ERROR_STOP=1 --username "$POSTGRES_USER" --dbname "$POSTGRES_DB" <<-EOSQL
    CREATE USER user WITH PASSWORD 'password';
    CREATE DATABASE mydb;
    GRANT ALL PRIVILEGES ON DATABASE mydb TO user;
EOSQL

ECHO "$POSTGRES_USER"