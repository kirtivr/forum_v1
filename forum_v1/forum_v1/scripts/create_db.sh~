#!/bin/bash
set -e

#  Run as: sudo -u postgres POSTGRES_USER=postgres POSTGRES_DB=forum_v1 ./create_db.sh

echo "Creating database: $POSTGRES_DB"
echo "user: $POSTGRES_USER"

psql -v ON_ERROR_STOP=1 --username "$POSTGRES_USER" <<-EOSQL
    CREATE USER horizon WITH PASSWORD 'nvjkefo412' CREATEDB;
    CREATE DATABASE forum_v1;
    ALTER ROLE horizon SET client_encoding TO 'utf8';
    ALTER ROLE horizon SET default_transaction_isolation TO 'read committed';
    ALTER ROLE horizon SET timezone TO 'Asia/Kolkata';
    GRANT ALL PRIVILEGES ON DATABASE modulo TO horizon;
EOSQL

