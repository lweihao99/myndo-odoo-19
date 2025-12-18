# # -*- coding: utf-8 -*-
# import logging
# import re
# from odoo import api, fields, models, _
# from odoo.exceptions import UserError
# from datetime import datetime, date
# import json
# import requests
# import string
# import random


# class amazon_error(models.Model):
# 	_inherit='myndo.error'
# 	amazon_api_profile=fields.Many2one("myndo_amazon_ads.api_profile")
# 	amazon_profile=fields.Many2one("myndo_amazon_ads.profile")
# 	amazon_area=fields.Many2one("myndo.area")


# class myndo_amazon_ads_api_profile_inherit(models.Model):
# 	_inherit='myndo_amazon_ads.api_profile'
# 	errors=fields.One2many('myndo.error','amazon_api_profile')
	
# 	def unlink(self):
# 		for line in self:
# 			for vi in line.errors:
# 				vi.unlink()
# 		out=super(myndo_amazon_ads_api_profile_inherit, self).unlink()
# 		return out


# class amazon_set(models.Model):
# 	_inherit='myndo.set'
# 	from_amazon_api=fields.Boolean("From amazon api",default=False)
# 	amazon_original_data=fields.Text(string='amazon original Data')
# 	amazon_profile=fields.Many2one("myndo_amazon_ads.profile")

# class myndo_amazon_ads_profile_inherit(models.Model):
# 	_inherit='myndo_amazon_ads.profile'
# 	errors=fields.One2many('myndo.error','amazon_profile')
# 	sets=fields.One2many('myndo.set','amazon_profile',string='amazon profile')
	
# 	def unlink(self):
# 		for line in self:
# 			for vi in line.errors:
# 				vi.unlink()
# 		out=super(myndo_amazon_ads_profile_inherit, self).unlink()
# 		return out


# class myndo_amazon_ads_api_profile_error(models.Model):
# 	_inherit='myndo_amazon_ads.api_profile'
# 	errors=fields.One2many('myndo.error','amazon_profile')


# class amazon_column(models.Model):
# 	_inherit='myndo.column'
# 	amazon_dsp_name=fields.Char('amazon dsp ADS name')
# 	amazon_sp_name=fields.Char('amazon sp ADS name')
# 	amazon_sb_name=fields.Char('amazon sb ADS name')
# 	amazon_sd_name=fields.Char('amazon sd ADS name')
# 	amazon_stv_name=fields.Char('amazon stv ADS name')
# 	amazon_name=fields.Char('amazon ADS name')
# 	amazon_group_by_name=fields.Char('amazon ADS group by name')
# 	amazon_dsp_group_by_name=fields.Char('amazon DSP group by name')
# 	# amazon_type=fields.Selection(selection=[('column', 'Column'),('group_by', 'Group By')])
# 	is_amazon_group_by_column=fields.Boolean("is amazon group by column",default=False)
# 	is_amazon_dsp_group_by_column=fields.Boolean("is amazon dsp group by column",default=False)


# 	@api.onchange('amazon_name')
# 	def _onchange_amazon_name(self):
# 		for rec in self:
# 			if rec=='' or rec==False:
# 				return {'required': 0}
# 			else:
# 				return {'required': 1}


# class myndo_amazon_ads_area_filter(models.Model):
# 	_name='myndo_amazon_ads.area_filter'
# 	area=fields.Many2one("myndo.area",string="area")
# 	col=fields.Many2one("myndo.column",string="Column")
# 	operatore=fields.Selection(selection=[( 'less','minore'),('greater','maggiore'),('equal','uguale'),('notequal','diverso'),('contain','contiene'),('notcontain','non contiene')],required=True)
# 	valfloat=fields.Float(string="Valore",default=0)
# 	valchar=fields.Char(string="Valore",default="")
	
# 	@api.depends('col')
# 	def _get_coltype(self):
# 		for rec in self:
# 			if rec.col:
# 				rec.coltype=rec.col.type.name
# 			else:
# 				rec.coltype=''
# 	coltype=fields.Char(string="Valore",compute="_get_coltype")
# 	@api.depends('col')
# 	def _get_display_name(self):
# 		for rec in self:
# 			rec.display_name=str(rec.col.name)+' '+str(rec.operatore)
# 			if rec.operatore=='equal' or rec.operatore=='not equal':
# 				rec.display_name=rec.display_name+' a '
# 			elif rec.operatore=='less' or rec.operatore=='greater':
# 				rec.display_name=rec.display_name+' di '
# 			else:
# 				rec.display_name=rec.display_name+' '
# 			if rec.col.type.name=='int' or rec.col.type.name=='float':
# 				rec.display_name=rec.display_name+str(rec.valfloat)
# 			else:
# 				rec.display_name=rec.display_name+str(rec.valchar)
# 	display_name=fields.Char("Name",compute="_get_display_name")


# class amazon_area(models.Model):
# 	_inherit='myndo.area'
# 	amazon_name=fields.Char('amazon ADS name')
# 	amazon_type=fields.Selection(selection=[('dsp', 'DSP'),('ads', 'ADS')])
# 	amazon_adProduct=fields.Selection(selection=[('SPONSORED_PRODUCTS', 'sponsored_products'),('SPONSORED_BRANDS', 'sponsored_brands'),('SPONSORED_DISPLAY', 'sponsored_display')])
# 	amazon_documentation_link=fields.Char('Documentation link')
# 	amazon_errors=fields.One2many('myndo.error','amazon_area')
# 	amazon_group_by_columns=fields.Many2many(comodel_name="myndo.column", relation="myndo_area_amazon_group_by_columns", column1="area_id", column2="column_id", domain="[('is_amazon_group_by_column', '=', True)]", string="Group by columns")
# 	amazon_ads_filters=fields.One2many('myndo_amazon_ads.area_filter','area',string='filters')
	
	
# 	def unlink(self):
# 		for line in self:
# 			for vi in line.amazon_errors:
# 				# raise UserError(_(vi))
# 				vi.unlink()
# 			for vi in line.amazon_ads_filters:
# 				# raise UserError(_(vi))
# 				vi.unlink()
# 		out=super(amazon_area, self).unlink()
# 		return out


# class myndo_amazon_ads_partner(models.Model):
# 	_inherit='res.partner'
# 	amazon_profiles=fields.One2many("myndo_amazon_ads.profile", "client", string="amazon accounts")
# 	amazon_areas=fields.Many2many(comodel_name='myndo.area', relation="myndo_amazon_ads_partner_areas", column1="partner_id", column2="area_id",string='Areas')
# 	amazon_unlocked=fields.Boolean('amazon ads')
# 	amazon_start_date=fields.Date('amazon ads start date')


# class myndo_amazon_ads_api_profile(models.Model):
# 	_name='myndo_amazon_ads.api_profile'
# 	active = fields.Boolean('Active', default=True)
# 	name = fields.Char('name')
# 	external_id = fields.Char('amazon id')
# 	refresh_token = fields.Text('Refresh token')
# 	_sql_constraints = [('ref_unique','unique(name)', 'name must be unique!')] 

# class myndo_amazon_ads_profile(models.Model):
# 	_name='myndo_amazon_ads.profile'
# 	active = fields.Boolean('Active', default=True)	
# 	name = fields.Char('name')
# 	amazon_account_number = fields.Char('amazon account number')
# 	external_id = fields.Char('amazon id')
# 	currencyCode=fields.Char('currencyCode')
# 	timeZone=fields.Char('timezone')
# 	status=fields.Char('status')
# 	account_type=fields.Char('account type')
# 	amazon_mrkt_id=fields.Char('amazon marketplace id')
# 	region=fields.Char('region')
# 	api_profile = fields.Many2one('myndo_amazon_ads.api_profile', string='API Profile')
# 	manager = fields.Many2one('myndo_amazon_ads.profile', string='Manager Profile')
# 	root_manager = fields.Many2one('myndo_amazon_ads.profile', string='Root Manager Profile')
# 	client=fields.Many2one('res.partner',string='Cliente')
# 	json_data=fields.Text('json_data')
# 	# report_url_expire_at=fields.Datetime('report url')
# 	is_manager=fields.Boolean('Manager account')
# 	_sql_constraints = [('ref_unique','unique(external_id)', 'amazon id must be unique!')] 


# class myndo_amazon_ads_api_profile_rels(models.Model):
# 	_inherit='myndo_amazon_ads.api_profile'
# 	profiles=fields.One2many('myndo_amazon_ads.profile','api_profile','Profiles')



# class myndo_amazon_ads_job(models.Model):
# 	_name='myndo_amazon_ads.job'
# 	active = fields.Boolean('Active', default=True)
# 	report_url=fields.Text('report url')
	
# 	def _compute_job_name(self):
# 		for rec in self:
# 			name=''
# 			if rec.profile:
# 				name=name+rec.profile.name
# 			if rec.area:
# 				name=name+'-'+rec.area.name
# 			if rec.start_date:
# 				name=name+'-'+rec.start_date.strftime("%Y/%m/%d")
# 			if rec.end_date:
# 				name=name+' to '+rec.end_date.strftime("%Y/%m/%d")
# 			rec.name=name
# 	name = fields.Char('name',compute=_compute_job_name)
# 	amazon_job_id = fields.Char('amazon job id')
# 	retries = fields.Integer('retries number',default=0)
# 	start_date = fields.Date('start date')
# 	end_date = fields.Date('end date')
# 	profile = fields.Many2one('myndo_amazon_ads.profile', string='Profile')
# 	manager_profile = fields.Many2one('myndo_amazon_ads.profile', string='Manager Profile')
# 	area = fields.Many2one('myndo.area', string='Area')
# 	state = fields.Selection([('0', 'Non ancora stato gestito'),('1', 'Lanciato su amazon'),('2', 'Report pronto'),('3', 'Dati salvati in myndo'),('-1', 'Errore report')],string='Status')