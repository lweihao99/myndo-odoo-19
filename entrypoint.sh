#!/bin/bash
set -e

# Debug
echo "DEBUG: DB_HOST=${DB_HOST}"
echo "DEBUG: DB_USER=${DB_USER}"
echo "DEBUG: DB_NAME=${DB_NAME}"
echo "DEBUG: ODOO_DB_PASS length=${#ODOO_DB_PASS}"
echo "DEBUG: PORT=${PORT}"

# Set PG env vars that Odoo reads natively
export PGHOST="${DB_HOST}"
export PGPORT="5432"
export PGUSER="${DB_USER}"
export PGPASSWORD="${ODOO_DB_PASS}"
export PGDATABASE="${DB_NAME}"

# Unset vars that could cause issues
unset DATABASE_URL DATABASE_PUBLIC_URL
unset POSTGRES_DB POSTGRES_USER POSTGRES_PASSWORD PGDATA

# Start Odoo
exec python3 /usr/bin/odoo \
    --config=/etc/odoo/odoo.conf \
    --http-port="${PORT:-8069}" \
    --http-interface=0.0.0.0 \
    "$@"
