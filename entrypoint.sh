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

# Check if myndo is already installed; if not, run init
MYNDO_INSTALLED=$(psql -h "${DB_HOST}" -U "${DB_USER}" -d "${DB_NAME}" -tAc \
    "SELECT state FROM ir_module_module WHERE name='myndo'" 2>/dev/null || echo "")

if [ "$MYNDO_INSTALLED" != "installed" ]; then
    echo "=== Myndo not installed (state='${MYNDO_INSTALLED}'), running init ==="
    python3 /usr/bin/odoo \
        --config=/etc/odoo/odoo.conf \
        -i base,myndo \
        --stop-after-init \
        --no-http 2>&1 || echo "=== Init finished ==="
else
    echo "=== Myndo already installed, skipping init ==="
fi

# Start Odoo normally
echo "=== Starting Odoo server ==="
exec python3 /usr/bin/odoo \
    --config=/etc/odoo/odoo.conf \
    --http-port="${PORT:-8069}" \
    --http-interface=0.0.0.0 \
    "$@"
