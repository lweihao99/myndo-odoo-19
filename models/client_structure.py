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

# Models for Client structure
class myndo_holding_agency(models.Model):
  _name = 'myndo.holding_agency'
  _description = 'Myndo Holding Agency'
  name=fields.Char(string='Name', required=True)
  agency_ids=fields.One2many('myndo.agency', 'holding_agency_id', string='Agencies')
  user_ids=fields.One2many('myndo.user_structure', 'holding_agency_id', string='Users')
  
class myndo_agency(models.Model):
  _name = 'myndo.agency'
  _description = 'Myndo holding client'
  name=fields.Char(string='Name', required=True)
  holding_agency_id=fields.Many2one('myndo.holding_agency', string='Holding Agency')
  holding_client_ids=fields.One2many('myndo.holding_client', 'agency_id', string='Holding Clients')
  user_ids=fields.One2many('myndo.user_structure', 'agency_id', string='Users')
  set_plan_template_ids=fields.Many2many('myndo.set_plan_template','agency_set_plan_template_rel','agency_id','set_plan_template_id', string='Set Plan Templates')

class myndo_holding_client(models.Model):
  _name = 'myndo.holding_client'
  _description = 'Myndo holding client'
  name=fields.Char(string='Name', required=True)
  agency_id=fields.Many2one('myndo.agency', string='Agency')
  client_ids=fields.One2many('myndo.client', 'holding_client_id', string='Clients')
  
class myndo_client(models.Model):
  _name = 'myndo.client'
  _description = 'Myndo client'
  name=fields.Char(string='Name', required=True)
  holding_client_id=fields.Many2one('myndo.holding_client', string='Holding Client')
  industry=fields.Char(string='Industry')
  country=fields.Char(string='Country')
  short_name=fields.Char(string='Short Name')
  vat_number=fields.Char(string='VAT Number')
  divisions_ids=fields.One2many('myndo.divisions', 'client_id', string='Divisions')
  client_subarea=fields.Many2one("myndo.subarea", string="client subarea")
  user_ids=fields.Many2many('myndo.user_structure','myndo_user_client_rel', 'client_id','user_id', string='Users')
  cross_area_ids=fields.Many2many("myndo.cross_area","cross_area_client_rel","client_id","cross_area_id",string="Cross Areas")
  
class myndo_brands(models.Model):
  _name = 'myndo.brands'
  _description = 'Myndo Brands'
  name=fields.Char(string='Name', required=True)
  division_id=fields.Many2one('myndo.divisions', string='Division')
  
class myndo_divisions(models.Model):
  _name = 'myndo.divisions'
  _description = 'Myndo Divisions'
  name=fields.Char(string='Name', required=True)
  short_name=fields.Char(string='Short Name')
  client_id=fields.Many2one('myndo.client', string='Client')
  brands=fields.One2many('myndo.brands', 'division_id', string='Brands')