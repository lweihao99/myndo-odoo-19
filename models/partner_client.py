# -*- coding: utf-8 -*-
from odoo import models, fields, api


class myndo_partner_client(models.Model):
    _name = 'myndo.partner_client'
    _description = 'Myndo Client Partnership Archive'
    _inherit = ['myndo.billing_mixin', 'mail.thread', 'mail.activity.mixin']
    _rec_name = 'name'
    _order = 'name'

    name = fields.Char(required=True, tracking=True)
    client_id = fields.Many2one(
        'myndo.client',
        string='Client',
        required=True,
        ondelete='restrict',
        tracking=True,
    )
    industry_id = fields.Many2one(
        'res.partner.industry', string='Industry')
    status = fields.Selection(
        [('active', 'Active'), ('inactive', 'Inactive')],
        default='inactive',
        required=True,
        tracking=True,
    )
    default_rebate = fields.Float(
        string='Default Rebate %',
        help='Default rebate percentage applied to this client (0-100).',
    )
    main_contact_id = fields.Many2one(
        'myndo.partner_client_contact',
        string='Main Contact',
        domain="[('client_id', '=', id)]",
    )
    dashboard_user_id = fields.Many2one(
        'res.users', string='Owner')

    tag_ids = fields.Many2many(
        'myndo.partner_tag',
        'myndo_partner_client_tag_rel',
        'client_id',
        'tag_id',
        string='Tags',
    )

    # One2many relationships
    contact_ids = fields.One2many(
        'myndo.partner_client_contact', 'client_id', string='Contacts')
    rebate_ids = fields.One2many(
        'myndo.partner_rebate', 'client_id', string='Rebates')
    account_ids = fields.One2many(
        'myndo.partner_account', 'client_id', string='Platform Accounts')
    saleshouse_period_ids = fields.One2many(
        'myndo.partner_saleshouse_period', 'client_id',
        string='Saleshouse Periods',
    )

    # Read-only pulls from client hierarchy
    division_ids = fields.Many2many(
        'myndo.divisions',
        compute='_compute_divisions_and_brands',
        string='Divisions',
    )
    brand_ids = fields.Many2many(
        'myndo.brands',
        compute='_compute_divisions_and_brands',
        string='Brands',
    )

    _sql_constraints = [
        ('client_unique',
         'UNIQUE(client_id)',
         'Each client can only have one partnership archive.'),
        ('default_rebate_range',
         'CHECK(default_rebate >= 0 AND default_rebate <= 100)',
         'Default rebate must be between 0 and 100.'),
    ]

    @api.depends('client_id', 'client_id.divisions_ids',
                 'client_id.divisions_ids.brands')
    def _compute_divisions_and_brands(self):
        for rec in self:
            divisions = rec.client_id.divisions_ids
            rec.division_ids = divisions
            rec.brand_ids = divisions.mapped('brands')

    @api.onchange('client_id')
    def _onchange_client_id(self):
        if self.client_id and not self.name:
            self.name = self.client_id.name


class myndo_partner_client_contact(models.Model):
    _name = 'myndo.partner_client_contact'
    _description = 'Myndo Client Partnership Contact'
    _order = 'surname, name'

    name = fields.Char(string='First Name', required=True)
    surname = fields.Char(string='Last Name')
    full_name = fields.Char(
        compute='_compute_full_name', store=True, string='Full Name')
    fiscal_code = fields.Char()
    role = fields.Char()
    email = fields.Char()
    phone = fields.Char()
    client_id = fields.Many2one(
        'myndo.partner_client',
        string='Client Archive',
        required=True,
        ondelete='cascade',
    )
    is_main = fields.Boolean(
        compute='_compute_is_main', string='Is Main Contact')

    @api.depends('name', 'surname')
    def _compute_full_name(self):
        for rec in self:
            parts = [rec.name or '', rec.surname or '']
            rec.full_name = ' '.join(p for p in parts if p).strip()

    @api.depends('client_id.main_contact_id')
    def _compute_is_main(self):
        for rec in self:
            rec.is_main = bool(
                rec.client_id and rec == rec.client_id.main_contact_id
            )


class myndo_partner_rebate(models.Model):
    _name = 'myndo.partner_rebate'
    _description = 'Myndo Client Rebate'

    client_id = fields.Many2one(
        'myndo.partner_client',
        string='Client Archive',
        required=True,
        ondelete='cascade',
    )
    media_type_id = fields.Many2one(
        'myndo.media_type', string='Media Type', required=True)
    rebate_percent = fields.Float(string='Rebate %', required=True)

    _sql_constraints = [
        ('client_media_unique',
         'UNIQUE(client_id, media_type_id)',
         'A rebate already exists for this client and media type.'),
        ('rebate_percent_range',
         'CHECK(rebate_percent >= 0 AND rebate_percent <= 100)',
         'Rebate percent must be between 0 and 100.'),
    ]


class myndo_partner_account(models.Model):
    _name = 'myndo.partner_account'
    _description = 'Myndo Client Platform Account'

    client_id = fields.Many2one(
        'myndo.partner_client',
        string='Client Archive',
        required=True,
        ondelete='cascade',
    )
    platform_id = fields.Many2one(
        'myndo.platform', string='Platform', required=True)
    external_account_id = fields.Char(
        string='External Account ID', required=True)
    external_account_name = fields.Char(string='External Account Name')

    _sql_constraints = [
        ('account_unique',
         'UNIQUE(client_id, platform_id, external_account_id)',
         'This platform account is already mapped to this client.'),
    ]


class myndo_partner_saleshouse_period(models.Model):
    _name = 'myndo.partner_saleshouse_period'
    _description = 'Myndo Client Saleshouse Period'
    _order = 'start_date desc'

    client_id = fields.Many2one(
        'myndo.partner_client',
        string='Client Archive',
        required=True,
        ondelete='cascade',
    )
    saleshouse_name = fields.Char(string='Saleshouse', required=True)
    start_date = fields.Date(required=True)
    end_date = fields.Date(required=True)

    _sql_constraints = [
        ('date_check',
         'CHECK(end_date >= start_date)',
         'End date must be on or after start date.'),
        ('client_saleshouse_unique',
         'UNIQUE(client_id, saleshouse_name)',
         'This saleshouse is already registered for the client.'),
    ]
