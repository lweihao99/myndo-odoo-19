#!/bin/bash
set -e

# Debug: print env vars (remove after testing)
echo "DEBUG: DB_HOST=${DB_HOST}"
echo "DEBUG: DB_USER=${DB_USER}"
echo "DEBUG: DB_NAME=${DB_NAME}"
echo "DEBUG: DB_PASSWORD length=${#DB_PASSWORD}"
echo "DEBUG: PORT=${PORT}"

# Set PG env vars that Odoo reads natively
export PGHOST="${DB_HOST}"
export PGPORT="5432"
export PGUSER="${DB_USER}"
export PGPASSWORD="${DB_PASSWORD}"
export PGDATABASE="${DB_NAME}"

# Unset vars that could cause issues
unset DATABASE_URL DATABASE_PUBLIC_URL
unset POSTGRES_DB POSTGRES_USER POSTGRES_PASSWORD PGDATA

# Start Odoo - let it read DB config from PG env vars, not CLI args
exec python3 /usr/bin/odoo \
    --config=/etc/odoo/odoo.conf \
    --http-port="${PORT:-8069}" \
    --http-interface=0.0.0.0 \
    "$@"
