#!/bin/bash
set -e

# Set PG env vars to our DB_* values (Odoo reads these directly)
export PGHOST="${DB_HOST}"
export PGPORT="5432"
export PGUSER="${DB_USER}"
export PGPASSWORD="${DB_PASSWORD}"
export PGDATABASE="${DB_NAME}"

# Unset vars that could cause parsing issues
unset DATABASE_URL DATABASE_PUBLIC_URL
unset POSTGRES_DB POSTGRES_USER POSTGRES_PASSWORD PGDATA

# Start Odoo
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
