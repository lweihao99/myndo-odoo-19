FROM odoo:19

USER root

# Copy custom addon
COPY . /mnt/extra-addons/myndo
RUN chown -R odoo:odoo /mnt/extra-addons/myndo

# Copy Odoo config
COPY odoo.conf /etc/odoo/odoo.conf
RUN chown odoo:odoo /etc/odoo/odoo.conf

# Patch: allow 'postgres' db user (Railway free tier only provides this user)
RUN sed -i "s/if config\['db_user'\] == 'postgres':/if False:/" /usr/lib/python3/dist-packages/odoo/service/server.py

# Create entrypoint script that injects DB env vars
COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

USER odoo

EXPOSE 8069

ENTRYPOINT ["/entrypoint.sh"]
