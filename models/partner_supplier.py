# -*- coding: utf-8 -*-
from odoo import models, fields, api


class myndo_partner_supplier(models.Model):
    _name = 'myndo.partner_supplier'
    _description = 'Myndo Supplier Partnership Archive'
    _inherit = ['myndo.billing_mixin', 'mail.thread', 'mail.activity.mixin']
    _rec_name = 'name'
    _order = 'name'

    name = fields.Char(required=True, tracking=True)
    agency_id = fields.Many2one(
        'myndo.agency',
        string='Agency',
        required=True,
        ondelete='restrict',
        tracking=True,
    )
    supplier_type = fields.Selection(
        [
            ('media_owner', 'Media Owner'),
            ('digital_agency', 'Digital Agency'),
            ('broadcaster', 'Broadcaster'),
            ('tech_platform', 'Tech Platform'),
            ('publisher', 'Publisher'),
        ],
        required=True,
        default='media_owner',
        tracking=True,
    )
    sourcing_type = fields.Selection(
        [('standard', 'Standard'), ('aggregated', 'Aggregated')],
        default='standard',
        required=True,
    )
    status = fields.Selection(
        [('active', 'Active'), ('inactive', 'Inactive')],
        default='inactive',
        required=True,
        tracking=True,
    )
    main_contact_id = fields.Many2one(
        'myndo.partner_supplier_contact',
        string='Main Contact',
        domain="[('supplier_id', '=', id)]",
    )
    rebate_goal_eoy = fields.Monetary(
        string='EOY Rebate Goal',
        currency_field='currency_id',
    )
    currency_id = fields.Many2one(
        'res.currency',
        string='Currency',
        default=lambda self: self.env.company.currency_id,
        required=True,
    )
    dashboard_user_id = fields.Many2one('res.users', string='Owner')

    tag_ids = fields.Many2many(
        'myndo.partner_tag',
        'myndo_partner_supplier_tag_rel',
        'supplier_id',
        'tag_id',
        string='Tags',
    )

    # One2many
    contact_ids = fields.One2many(
        'myndo.partner_supplier_contact', 'supplier_id', string='Contacts')
    agreement_ids = fields.One2many(
        'myndo.partner_agreement', 'supplier_id', string='Agreements')

    active_agreement_count = fields.Integer(
        compute='_compute_active_agreement_count',
        store=True,
        string='Active Agreements',
    )

    _sql_constraints = [
        ('agency_name_unique',
         'UNIQUE(agency_id, name)',
         'Supplier name must be unique per agency.'),
    ]

    @api.depends('agreement_ids.state')
    def _compute_active_agreement_count(self):
        for rec in self:
            rec.active_agreement_count = len(
                rec.agreement_ids.filtered(lambda a: a.state == 'active')
            )


class myndo_partner_supplier_contact(models.Model):
    _name = 'myndo.partner_supplier_contact'
    _description = 'Myndo Supplier Partnership Contact'
    _order = 'surname, name'

    name = fields.Char(string='First Name', required=True)
    surname = fields.Char(string='Last Name')
    full_name = fields.Char(
        compute='_compute_full_name', store=True, string='Full Name')
    fiscal_code = fields.Char()
    role = fields.Char()
    email = fields.Char()
    phone = fields.Char()
    supplier_id = fields.Many2one(
        'myndo.partner_supplier',
        string='Supplier Archive',
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

    @api.depends('supplier_id.main_contact_id')
    def _compute_is_main(self):
        for rec in self:
            rec.is_main = bool(
                rec.supplier_id and rec == rec.supplier_id.main_contact_id
            )


class myndo_partner_agreement(models.Model):
    _name = 'myndo.partner_agreement'
    _description = 'Myndo Supplier Agreement'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'end_date desc, name'

    name = fields.Char(required=True, tracking=True)
    supplier_id = fields.Many2one(
        'myndo.partner_supplier',
        string='Supplier Archive',
        required=True,
        ondelete='cascade',
        tracking=True,
    )
    start_date = fields.Date(required=True, tracking=True)
    end_date = fields.Date(required=True, tracking=True)
    media_type_id = fields.Many2one(
        'myndo.media_type', string='Media Type')
    state = fields.Selection(
        [
            ('draft', 'Draft'),
            ('active', 'Active'),
            ('expired', 'Expired'),
        ],
        string='Status',
        default='draft',
        compute='_compute_state',
        store=True,
        tracking=True,
    )
    attachment_ids = fields.Many2many(
        'ir.attachment',
        'myndo_partner_agreement_attachment_rel',
        'agreement_id',
        'attachment_id',
        string='Attachments',
    )
    notes = fields.Text()

    _sql_constraints = [
        ('date_check',
         'CHECK(end_date >= start_date)',
         'End date must be on or after start date.'),
    ]

    @api.depends('start_date', 'end_date')
    def _compute_state(self):
        today = fields.Date.context_today(self)
        for rec in self:
            if not rec.start_date or not rec.end_date:
                rec.state = 'draft'
            elif rec.end_date < today:
                rec.state = 'expired'
            elif rec.start_date <= today <= rec.end_date:
                rec.state = 'active'
            else:
                rec.state = 'draft'

    @api.model
    def _cron_refresh_agreement_state(self):
        agreements = self.search([('state', '!=', 'expired')])
        agreements._compute_state()
        agreements.flush_model(['state'])
