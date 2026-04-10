# -*- coding: utf-8 -*-
from odoo import models, fields, api
from random import randint


class myndo_billing_mixin(models.AbstractModel):
    _name = 'myndo.billing_mixin'
    _description = 'Myndo Billing Mixin'

    company_name = fields.Char(string='Company Name')
    vat_id = fields.Char(string='VAT ID')
    fiscal_code = fields.Char(string='Fiscal Code')
    pec_sdi = fields.Char(string='PEC / SDI')
    payment_terms = fields.Char(string='Payment Terms')
    address = fields.Char(string='Address')
    postal_code = fields.Char(string='Postal Code')
    city = fields.Char(string='City')
    country_id = fields.Many2one('res.country', string='Country')


class myndo_media_type(models.Model):
    _name = 'myndo.media_type'
    _description = 'Myndo Media Type'
    _order = 'sequence, name'

    name = fields.Char(required=True)
    code = fields.Char(help='Short code used for data import matching.')
    sequence = fields.Integer(default=10)
    active = fields.Boolean(default=True)

    _sql_constraints = [
        ('name_unique', 'UNIQUE(name)',
         'Media type name must be unique.'),
    ]


def _default_tag_color():
    return randint(1, 11)


class myndo_partner_tag(models.Model):
    _name = 'myndo.partner_tag'
    _description = 'Myndo Partner Tag'
    _order = 'name'

    name = fields.Char(required=True)
    color = fields.Integer(default=_default_tag_color)
    active = fields.Boolean(default=True)

    _sql_constraints = [
        ('name_unique', 'UNIQUE(name)',
         'Tag name must be unique.'),
    ]
