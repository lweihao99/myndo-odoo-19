# -*- coding: utf-8 -*-
import logging
import re
from odoo import api, fields, models, _
from odoo.exceptions import UserError
from datetime import datetime, date
import json
import requests
import string
import random

class myndo_plaform(models.Model):
    _name = "myndo.platform"
    _description = "Myndo Platforms"

    name = fields.Char(string="Platform name", required=True)

# class myndo_amazon_standardise_platforms_column(models.Model):
#     _name = "myndo.amazon_standardise_platforms_column"
#     _description = "Myndo Amazon Standardise Platforms Column"
    
#     _rec_name = 'platform_column_name'

#     # name = fields.Many2one("myndo.platform", string="Related Platform")
#     platform_column_name = fields.Char(string="External Column Name", required=True, help="The key/name used in the platform's API or export")
#     # rel_column = fields.Many2one("myndo.amazon_platform_column_usage", string="Related Column")
#     rel_platform = fields.Many2one("myndo.platform", string="Related Platform")
#     platform_column_type = fields.Selection([
#         ('string', 'String'),
#         ('int', 'Integer'),
#         ('float', 'Float'),
#         ('date', 'Date'),
#         ('datetime', 'Datetime'),
#         ('boolean', 'Boolean'),
#         ('array', 'Array/List'),
#         ('object', 'Object/JSON'),
#     ], string="External Data Type", default='string')
#     standardise_column = fields.One2many("myndo.amazon_platform_column_usage","platform_id", string="Mapped Standardised Column")
    
class myndo_standardise_platforms_column(models.Model):
    _name = "myndo.standardise_platforms_column"
    _description = "Myndo Amazon Standardise Platforms Column"
    
    _rec_name = 'platform_column_name'

    # name = fields.Many2one("myndo.platform", string="Related Platform")
    platform_id = fields.Many2one("myndo.platform", string="Related Platform")
    platform_column_name = fields.Char(string="External Column Name", required=True, help="The key/name used in the platform's API or export")
    # rel_column = fields.Many2one("myndo.platform_column_usage", string="Related Column")
    rel_platform = fields.Many2one("myndo.platform", string="Related Platform")
    platform_column_type = fields.Selection([
        ('string', 'String'),
        ('int', 'Integer'),
        ('float', 'Float'),
        ('date', 'Date'),
        ('datetime', 'Datetime'),
        ('boolean', 'Boolean'),
        ('array', 'Array/List'),
        ('object', 'Object/JSON'),
    ], string="External Data Type", default='string')
    standardise_column = fields.One2many("myndo.platform_column_usage","platform_id", string="Mapped Standardised Column")