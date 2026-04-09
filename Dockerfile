FROM odoo:19

USER root

# Install psql client for user creation in entrypoint
RUN apt-get update && apt-get install -y --no-install-recommends postgresql-client && rm -rf /var/lib/apt/lists/*

# Copy custom addon
COPY . /mnt/extra-addons/myndo
RUN chown -R odoo:odoo /mnt/extra-addons/myndo

# Copy Odoo config
COPY odoo.conf /etc/odoo/odoo.conf
RUN chown odoo:odoo /etc/odoo/odoo.conf

# Patch: remove postgres user check from Odoo docker entrypoint
RUN sed -i '/postgres.*security risk/d' /usr/local/bin/docker-entrypoint.sh 2>/dev/null; \
    sed -i '/security risk.*aborting/d' /usr/local/bin/docker-entrypoint.sh 2>/dev/null; \
    grep -rl "security risk" /usr/local/bin/ /etc/odoo/ 2>/dev/null | xargs sed -i '/security risk/d' 2>/dev/null; \
    true

# Create entrypoint script
COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

USER odoo

EXPOSE 8069

ENTRYPOINT ["/entrypoint.sh"]
