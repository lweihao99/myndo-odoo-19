#!/bin/bash
set -e

# Unset Railway/Postgres env vars that Odoo 19 auto-reads
unset PGPORT PGHOST PGUSER PGPASSWORD PGDATABASE PGDATA
unset DATABASE_URL DATABASE_PUBLIC_URL
unset POSTGRES_DB POSTGRES_USER POSTGRES_PASSWORD

# Start Odoo directly with postgres user, bypassing docker-entrypoint.sh check
exec python3 /usr/bin/odoo \
    --config=/etc/odoo/odoo.conf \
    --db_host="${DB_HOST}" \
    --db_port=5432 \
    --db_user="${DB_USER}" \
    --db_password="${DB_PASSWORD}" \
    --database="${DB_NAME}" \
    --http-port="${PORT:-8069}" \
    --http-interface=0.0.0.0 \
    "$@"
