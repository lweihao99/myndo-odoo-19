#!/bin/bash
set -e

# Start Odoo with database connection from environment variables
exec odoo \
    --config=/etc/odoo/odoo.conf \
    --db_host="${HOST}" \
    --db_port=5432 \
    --db_user="${USER}" \
    --db_password="${PASSWORD}" \
    --http-port="${PORT:-8069}" \
    "$@"
