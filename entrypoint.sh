#!/bin/bash
set -e

# Unset Railway/Postgres env vars that Odoo 19 auto-reads and fails to parse
unset PGPORT PGHOST PGUSER PGPASSWORD PGDATABASE PGDATA
unset DATABASE_URL DATABASE_PUBLIC_URL
unset POSTGRES_DB POSTGRES_USER POSTGRES_PASSWORD

# Create a non-postgres superuser for Odoo (Railway only provides 'postgres' user)
export PGPASSWORD="${DB_PASSWORD}"
ODOO_DB_USER="odoo"
ODOO_DB_PASS="odoo_$(echo "${DB_PASSWORD}" | head -c 16)"

# Try to create odoo user, ignore if already exists
psql -h "${DB_HOST}" -p 5432 -U "${DB_USER}" -d "${DB_NAME}" -c \
    "DO \$\$ BEGIN
        IF NOT EXISTS (SELECT FROM pg_roles WHERE rolname = '${ODOO_DB_USER}') THEN
            CREATE ROLE ${ODOO_DB_USER} WITH LOGIN SUPERUSER PASSWORD '${ODOO_DB_PASS}';
        END IF;
    END \$\$;" 2>/dev/null || true

unset PGPASSWORD

# Start Odoo with the new odoo user
exec odoo \
    --config=/etc/odoo/odoo.conf \
    --db_host="${DB_HOST}" \
    --db_port=5432 \
    --db_user="${ODOO_DB_USER}" \
    --db_password="${ODOO_DB_PASS}" \
    --database="${DB_NAME}" \
    --http-port="${PORT:-8069}" \
    --http-interface=0.0.0.0 \
    "$@"
