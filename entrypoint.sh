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

# Install/update myndo module (also initializes base on first run)
# Use -i to install if not present, -u to update if already installed
echo "=== Installing/updating myndo module ==="
python3 /usr/bin/odoo \
    --config=/etc/odoo/odoo.conf \
    -i base,myndo \
    --stop-after-init \
    --no-http 2>&1 || echo "=== Init finished (errors above may be ignored if module already installed) ==="

# Start Odoo normally
echo "=== Starting Odoo server ==="
exec python3 /usr/bin/odoo \
    --config=/etc/odoo/odoo.conf \
    --http-port="${PORT:-8069}" \
    --http-interface=0.0.0.0 \
    "$@"
