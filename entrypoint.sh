#!/bin/bash
set -e

# Set PG env vars that Odoo reads natively
export PGHOST="${DB_HOST}"
export PGPORT="5432"
export PGUSER="${DB_USER}"
export PGPASSWORD="${ODOO_DB_PASS}"
export PGDATABASE="${DB_NAME}"

# Unset vars that could cause issues
unset DATABASE_URL DATABASE_PUBLIC_URL
unset POSTGRES_DB POSTGRES_USER POSTGRES_PASSWORD PGDATA

# Initialize database if not yet done (check for ir_module_module table)
python3 /usr/bin/odoo \
    --config=/etc/odoo/odoo.conf \
    --init=base \
    --stop-after-init \
    --http-port="${PORT:-8069}" \
    --http-interface=0.0.0.0 2>&1 || true

# Start Odoo
exec python3 /usr/bin/odoo \
    --config=/etc/odoo/odoo.conf \
    --http-port="${PORT:-8069}" \
    --http-interface=0.0.0.0 \
    "$@"
