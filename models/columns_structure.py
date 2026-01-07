# -*- coding: utf-8 -*-
import logging
import re
from odoo import api, fields, models, _
from odoo.exceptions import UserError
from datetime import datetime,date
import json
import requests
import string
import random

# dimensions, metrics, alg
class myndo_columns_structure(models.Model):
  _name = 'myndo.columns_structure'
  _description = 'Myndo Columns Structure'
  name=fields.Char(string='Name', required=True)
  short_name=fields.Char(string='Short Name')
  description=fields.Text(string='Description')
  type=fields.Selection([
    ('float', 'Float'),
    ('int', 'Integer'),
    ('validator', 'Validator'),
    ('string', 'String'),
    ('date', 'Date'),
    ('boolean', 'Boolean'),
  ], string='Data Type', required=True)
  accept_null=fields.Boolean(string='Accept Null Value', default=True)
  base_type=fields.Selection([
    ('dimension', 'Dimension'),
    ('metric', 'Metric'),
    ('algorithm', 'Algorithm'),
  ], string='Base Type', required=True)
  
  rel_areas=fields.Many2many('myndo.subarea','columns_structure_area_rel','column_id','area_id', string='Related Areas')
  rel_deconcat_rule_value=fields.One2many('myndo.deconcat_rule_value','column_id', string='Related Deconcat Rule Values')
  rel_deconcat_rule=fields.Many2one('myndo.deconcat_rules', string='Related Deconcat Rule')
  associated_rule_ids = fields.Many2many('myndo.deconcat_rules',compute='_compute_associated_rules',string='Associated Deconcat Rules',store=False)
  subarea_usage_ids = fields.One2many('myndo.subarea_column_usage','column_id',string='Used in Subareas')
  set_template_usage_ids = fields.One2many('myndo.set_template_columns_usage','column_id',string='Used in Templates')
  standardise_platforms_column_ids = fields.One2many("myndo.platform_column_usage", "column_id", string="Related Platforms Columns")
  validator_items = fields.One2many('myndo.validator_items', 'column_id', string='Validator Items')
  downloader_template_usage_ids = fields.One2many("myndo.downloader_template_columns_usage", "column_id", string="Downloader Template Columns")
  active = fields.Boolean(default=True)
  fixed_db_col = fields.Boolean(string="Is Fixed DB Column", help="If true, this column is part of the core database structure.")
  fixed_db_col_matchable_in_cross = fields.Boolean(string="Matchable in Cross Area", help="If true, this column can be used as a join key in cross-area operations.")
  cross_column_usage_ids = fields.One2many("myndo.cross_area_columns", "column_id", string="Cross Area Usages")
  
  connected_platforms = fields.Char(string="Connected Platforms", compute="_compute_connected_platforms", store=True)

  @api.depends("standardise_platforms_column_ids.platform_name_ref")
  def _compute_connected_platforms(self):
      for rec in self:
          names = rec.standardise_platforms_column_ids.mapped("platform_name_ref")
          rec.connected_platforms = ", ".join(list(set([n for n in names if n])))

  @api.depends('rel_deconcat_rule', 'rel_deconcat_rule_value.deconcat_rule_id')
  def _compute_associated_rules(self):
        for record in self:
            mapped_rules = record.rel_deconcat_rule_value.mapped('deconcat_rule_id')
            record.associated_rule_ids = mapped_rules
            
class myndo_column_usage(models.Model):
  _name = "myndo.column_usage"
  _description = "Myndo Column Usage"
  usage_type = fields.Selection([
      ('dimension', 'Dimension'),
      ('metric', 'Metric'),
      ('algorithm', 'Algorithm'),
  ], string='Column Type', required=True)
  decorator=fields.Selection([
        ('none', 'None'),
        ('currency', 'Currency'),
        ('int', 'Integer'),
        ('float', 'Float'),
        ('percent', 'Percentage'),
    ], string='Column decorator')
  group_fn=fields.Selection([
    ('none', 'None'),
    ('text', 'Text'),
    ('select', 'Select'),
    ('range', 'Range'),
  ], string='Group Function')
  
  js_code = fields.Text(string='JS Code')
  is_multiple=fields.Boolean(string='Is Multi in Plan', default=False)
  hide_total=fields.Boolean(string='Hide Total', default=False)
  
  def action_edit_algorithm(self):
        """ open window to edit js code """
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'name': _('Edit Algorithm Logic'),
            'res_model': self._name,
            'res_id': self.id,
            'view_mode': 'form',
            'view_id': False,
            'target': 'new',
        }
  

class myndo_subarea_column_usage(models.Model):
    _name = "myndo.subarea_column_usage"
    _description = "Myndo Subarea Column Usage"
    _inherit = "myndo.column_usage"
    _rec_name = "column_id"
    
    subarea_id = fields.Many2one("myndo.subarea", string="Subarea", ondelete='cascade')
    column_id = fields.Many2one("myndo.columns_structure", string="Column", ondelete='cascade')

class myndo_set_template_columns_usage(models.Model):
    _name = "myndo.set_template_columns_usage"
    _description = "Myndo Template Columns"
    _inherit = "myndo.column_usage"
    _rec_name = "column_id"
    
    template_id = fields.Many2one("myndo.set_plan_template", string="Template", ondelete='cascade')
    column_id = fields.Many2one("myndo.columns_structure", string="Column", ondelete='cascade')
    
# class myndo_amazon_platform_column_usage(models.Model):
#     _name = "myndo.amazon_platform_column_usage"
#     _description = "Myndo Template Columns"
#     _inherit = "myndo.column_usage"
    
#     # amazon_column_id = fields.One2Many("myndo.amazon_standardise_platforms_column","rel_column", string="Template", ondelete='cascade')
#     column_id = fields.Many2one("myndo.columns_structure", string="Column", ondelete='cascade')
#     platform_id = fields.Many2one("myndo.amazon_standardise_platforms_column", string="Platform", ondelete='cascade')
#     original_column_name = fields.Char(string="Original Platform Column Name",related='platform_id.platform_column_name',store=True,readonly=True)
#     platform_name_ref = fields.Char(string="Platform Name",related='platform_id.name.name',readonly=True)
    
class myndo_platform_column_usage(models.Model):
    _name = "myndo.platform_column_usage"
    _description = "Myndo Template Columns"
    _inherit = "myndo.column_usage"
    _rec_name = "column_id"
    
    # column_id = fields.One2Many("myndo.standardise_platforms_column","rel_column", string="Template", ondelete='cascade')
    column_id = fields.Many2one("myndo.columns_structure", string="Column", ondelete='cascade')
    platform_id = fields.Many2one("myndo.standardise_platforms_column", string="Platform", ondelete='cascade')
    original_column_name = fields.Char(string="Original Platform Column Name",related='platform_id.platform_column_name',store=True,readonly=True)
    platform_name_ref = fields.Char(string="Platform Name",related='platform_id.platform_id.name',readonly=True)
    
class myndo_downloader_template_columns_usage(models.Model):
    _name = "myndo.downloader_template_columns_usage"
    _description = "Myndo Template Columns"
    _inherit = "myndo.column_usage"
    _rec_name = "column_id"
    
    template_id = fields.Many2one("myndo.downloader_template", string="Template", ondelete='cascade')
    column_id = fields.Many2one("myndo.columns_structure", string="Column", ondelete='cascade')