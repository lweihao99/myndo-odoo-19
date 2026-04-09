#!/bin/bash
set -e

# Render provides PORT env var (default 10000)
# DB connection via DB_* env vars to avoid conflicts with system vars
exec odoo \
    --config=/etc/odoo/odoo.conf \
    --db_host="${DB_HOST}" \
    --db_port=5432 \
    --db_user="${DB_USER}" \
    --db_password="${DB_PASSWORD}" \
    --database="${DB_NAME}" \
    --http-port="${PORT:-8069}" \
    --http-interface=0.0.0.0 \
    "$@"
