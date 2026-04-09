FROM odoo:19

USER root

# Copy custom addon
COPY . /mnt/extra-addons/myndo
RUN chown -R odoo:odoo /mnt/extra-addons/myndo

# Copy Odoo config
COPY odoo.conf /etc/odoo/odoo.conf
RUN chown odoo:odoo /etc/odoo/odoo.conf

# Patch: disable postgres user check in Odoo source
RUN sed -i "s/if (config\['db_user'\] or os.environ.get('PGUSER')) == 'postgres':/if False:/" /usr/lib/python3/dist-packages/odoo/cli/server.py

# Create entrypoint script
COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

USER odoo

EXPOSE 8069

ENTRYPOINT ["/entrypoint.sh"]
