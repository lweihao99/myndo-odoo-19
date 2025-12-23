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


class myndo_user_structure(models.Model):
    _name = "myndo.user_structure"
    _description = "Myndo User Data"
    name = fields.Char(string="Name", required=True)
    surname = fields.Char(string="Surname", required=True)
    email = fields.Char(string="Email", required=False)
    role = fields.Selection([
            ("admin", "Admin"),
            ("manager", "Manager"),
            ("user", "User"),
        ],string="Role",required=True)
    myndo_button = fields.Boolean(string="Myndo Button activate", default=False)
    # Relations
    holding_agency_id = fields.Many2one("myndo.holding_agency", string="Holding Agency")
    agency_id = fields.Many2one("myndo.agency", string="Agency")
    client_id = fields.Many2many("myndo.client", "myndo_user_client_rel", "user_id", "client_id", string="Client")
    # TOOLDS
    homepage_tool = fields.Boolean("Homepage Tool")
    planner_tool = fields.Boolean("Planner Tool")
    owner_tool = fields.Boolean("Owner Tool")
    calendar_tool = fields.Boolean("Calendar Tool")
    sources_tool = fields.Boolean("Source Tool")
    planner_utilities_tool = fields.Boolean("Planner utils Tool")
    connector_tool = fields.Boolean("Connector Tool")
    naming_tool = fields.Boolean("Naming Tool")
    reporting_tool = fields.Boolean("Reporting Tool")
    reconciliation_tool = fields.Boolean("Reconciliation Tool")
    dashboard_tool = fields.Boolean("Dashboard Tool")
    myndodashboard_tool = fields.Boolean("Myboard Tool")
    partners_tool = fields.Boolean("Partners Tool")
    data_validation_tool = fields.Boolean("Data valid Tool")
    forecast_tool = fields.Boolean("Forecast Tool")
    governance_tool = fields.Boolean("Governance Tool")

    def action_clear_clients(self):
        for record in self:
            record.client_id = [(5, 0, 0)]

        return {
            "type": "ir.actions.client",
            "tag": "reload",
        }

    # resetta agency quando si cambia holding agency
    @api.onchange("holding_agency_id")
    def _onchange_holding_agency(self):
        self.agency_id = False

    # quando si cambia agency resetta clients
    @api.onchange("agency_id")
    def _onchange_agency(self):
        self.client_id = [(5, 0, 0)]


class myndo_area(models.Model):
    _name = "myndo.area"
    _description = "Myndo Area"
    name = fields.Char(string="Name", required=True)
    clean_name = fields.Char(string="Display Name")
    description = fields.Text(string="Description")
    required_columns = fields.Many2many("myndo.columns_structure","myndo_area_columns_rel","area_id","column_id",string="Required Columns")
    rel_subareas = fields.Many2many("myndo.subarea","area_subarea_rel","area_id","subarea_id",string="Related Subareas")
    validator_items = fields.Many2many("myndo.validator_items", "validator_items_area_rel", "area_id", "validator_items_id",string="Validator Items")
    # rel_tag_colors = fields.Many2many("myndo.area_tag_color","area_tag_color_rel","area_id","tag_id",string="Related Tag Colors")
    cross_area_ids = fields.One2many("myndo.cross_area","area_id",string="Cross Areas")
    
# class myndo_area_tag_color(models.Model):
#     _name = "myndo.area_tag_color"
#     _description = "Myndo Area Tag Color"
#     name = fields.Char(string="Tag name", required=True)
#     color = fields.Integer(string="Color", required=True,default=_default_color)
#     active = fields.Boolean(string="Active", default=True)
    
#     rel_areas = fields.Many2many("myndo.area","area_tag_color_rel","tag_id","area_id",string="Related Areas")

#     # def _default_color(self):
#     #     return random.randint(1, 16777215)

class myndo_subarea(models.Model):
    _name = "myndo.subarea"
    _description = "Myndo Subarea"
    name = fields.Char(string="Name", required=True)
    clean_name = fields.Char(string="Display Name")
    description = fields.Text(string="Description")
    rel_areas = fields.Many2many("myndo.area","area_subarea_rel","subarea_id","area_id",string="Related Areas")
    clients_ids = fields.Many2many("myndo.client","subarea_clients_rel","subarea_id","client_id",string="Clients")
    required_columns = fields.One2many("myndo.subarea_column_usage","subarea_id",string="Required Columns")

    show_profile = fields.Boolean("Mostra profili")
    show_customer = fields.Boolean("Mostra cliente")
    show_origin = fields.Boolean("Mostra provenienza")
    only_common_cols = fields.Boolean("Solo colonne in comune", default=True)
    active = fields.Boolean("active", default=True)
    rel_cross_area_ids = fields.One2many("myndo.cross_area","area_id",string="Cross Areas")

#  cross between 2 areas 
class myndo_cross_area(models.Model):
    _name = "myndo.cross_area"
    _description = "Myndo Cross Area"
    name = fields.Char(string="Name", required=True)
    clean_name = fields.Char(string="Display Name", required=True)
    clients_ids = fields.Many2many("myndo.client","cross_area_clients_rel","cross_area_id","client_id",string="Clients")
    area_id = fields.Many2one("myndo.area", string="Area")
    keep_only_matched_rows = fields.Boolean(string="Keep only matched rows", default=False)
    operation_ids = fields.One2many("myndo.cross_area_operation", "cross_area_id", string="Operations")
    final_col_ids = fields.One2many("myndo.cross_area_columns", "cross_area_id", string="Final Columns")
    filter_ids = fields.Many2many("myndo.cross_area_operation_filter", "cross_area_filters_rel", "cross_area_id", "filter_id", string="Filters")
    
    # create final columns
    def action_create_cols_combo(self):
        self.ensure_one()
        self.final_col_ids.unlink()
        
        new_cols = []
        if self.area_id:
            for col in self.area_id.required_columns:
                new_cols.append({
                    'cross_area_id': self.id,
                    'area_id': self.area_id.id,
                    'column_id': col.id
                })
        
        for op in self.operation_ids:
            if op.main_area_id:
                for col in op.main_area_id.required_columns:
                    new_cols.append({
                        'cross_area_id': self.id,
                        'area_id': op.main_area_id.id,
                        'column_id': col.id
                    })
        
        if new_cols:
            self.env['myndo.cross_area_columns'].create(new_cols)


class myndo_cross_area_operation(models.Model):
    _name = "myndo.cross_area_operation"
    _description = "Myndo Cross Area Operation"
    name = fields.Char(string="Name", required=True)
    cross_area_id = fields.Many2one("myndo.cross_area", string="Cross Area",ondelete='cascade')
    main_area_id = fields.Many2one("myndo.area", string="Area to Merge")
    only_matched = fields.Boolean(string="Keep only matched rows", default=True)
    cols_to_match_ids = fields.Many2many("myndo.columns_structure", string="Merge based on columns")
    filter_ids = fields.Many2many("myndo.cross_area_operation_filter", relation="myndo_cross_area_op_filters_rel", string="Operation Filters")
    
    cols_to_match_domain_ids = fields.Many2many("myndo.columns_structure", compute="_compute_cols_to_match_domain")
    
    @api.depends('main_area_id', 'cross_area_id.area_id')
    def _compute_cols_to_match_domain(self):
        fixed_cols = self.env['myndo.columns_structure'].search([
            ('fixed_db_col', '=', True),
            ('fixed_db_col_matchable_in_cross', '=', True)
        ])
        
        for rec in self:
            if not rec.cross_area_id or not rec.main_area_id:
                rec.cols_to_match_domain_ids = fixed_cols
                continue

            area_a_cols = rec.cross_area_id.area_id.required_columns.ids
            area_b_cols = rec.main_area_id.required_columns.ids
            
            common_col_ids = set(area_a_cols) & set(area_b_cols)
            final_ids = list(common_col_ids | set(fixed_cols.ids))
            rec.cols_to_match_domain_ids = [(6, 0, final_ids)]

class myndo_cross_area_columns(models.Model):
    _name = "myndo.cross_area_columns"
    _description = "Myndo Cross Area Columns"
    _rec_name = 'display_name'
    cross_area_id = fields.Many2one("myndo.cross_area", ondelete='cascade')
    area_id = fields.Many2one("myndo.area", string="Source Area")
    column_id = fields.Many2one("myndo.columns_structure", string="Column")
    split_between_matches = fields.Boolean(string="Split between matches", default=True)
    is_final_col = fields.Boolean(string="Is Final Column", default=True)
    display_name = fields.Char(string="Display Name", compute='_compute_display_name')
    
    @api.depends('area_id', 'column_id')
    def _compute_display_name(self):
        for rec in self:
            area_name = rec.area_id.name or '?'
            col_name = rec.column_id.name or '?'
            rec.display_name = f"{area_name} - {col_name}"
    
class myndo_cross_area_operation_filter(models.Model):
    _name = "myndo.cross_area_operation_filter"
    _description = "Myndo Cross Area Operation Filter"
    _rec_name = 'display_name'
    
    column_id = fields.Many2one("myndo.columns_structure", string="Column", required=True)
    operator = fields.Selection([
        ('less', 'Minore (<)'),
        ('greater', 'Maggiore (>)'),
        ('equal', 'Uguale (=)'),
        ('notequal', 'Diverso (!=)'),
        ('contain', 'Contiene'),
        ('notcontain', 'Non contiene')
    ], string="Operator", required=True)
    val_float = fields.Float(string="Value (Numeric)", default=0.0)
    val_char = fields.Char(string="Value (Text)", default="")
    col_type = fields.Selection(related="column_id.type", string="Column Type", readonly=True)
    display_name = fields.Char(string="Display Name", compute='_compute_display_name')
    
    @api.depends('column_id', 'operator', 'val_float', 'val_char')
    def _compute_display_name(self):
        for rec in self:
            is_numeric = rec.col_type in ['float', 'int']
            val = str(rec.val_float) if is_numeric else (rec.val_char or '')
            
            op_dict = dict(self._fields['operator'].selection)
            op_label = op_dict.get(rec.operator, rec.operator)
            
            rec.display_name = f"{rec.column_id.name} {op_label} {val}"


class myndo_deconcat_rules(models.Model):
    _name = "myndo.deconcat_rules"
    _description = "Myndo Deconcat Rules"
    name = fields.Char(string="Name", required=True)
    description = fields.Text(string="Description")
    cols_values = fields.One2many("myndo.deconcat_rule_value", "deconcat_rule_id", string="Columns Values")
    reconciliation_std_columns = fields.One2many("myndo.columns_structure","rel_deconcat_rule",string="Reconciliation Standard Columns")
    from_col = fields.Many2one("myndo.columns_structure", string="Colonne Necessarie")
    management_fee_col = fields.Many2one("myndo.columns_structure", string="Colonna management fee")

    include_jobnumber = fields.Boolean(string="include jobnumber")
    include_client = fields.Boolean(string="include client")
    include_purchase_order = fields.Boolean(string="include purchase order")
    include_brand = fields.Boolean(string="include brand")
    include_country = fields.Boolean(string="include country")
    include_unicode = fields.Boolean(string="include unicode")

    separator = fields.Char("plan naming separator")
    replace_spaces = fields.Char("plan naming space replace")


class myndo_deconcat_rule_value(models.Model):
    _name = "myndo.deconcat_rule_value"
    value = fields.Char(string="value")
    deconcat_rule_id = fields.Many2one("myndo.deconcat_rules", string="Rule")
    column_id = fields.Many2one("myndo.columns_structure", string="Colonna")

    @api.constrains("value", "deconcat_rule_id", "column_id")
    def _check_unique_value_per_rule_and_col(self):
        for record in self:
            if record.value and record.deconcat_rule_id and record.column_id:
                domain = [
                    ("value", "=", record.value),
                    ("deconcat_rule_id", "=", record.deconcat_rule_id.id),
                    ("column_id", "=", record.column_id.id),
                ]

                if record.id:
                    domain.append(('id', '!=', record.id))
                
                existing = self.search(domain)
                if existing:
                    raise UserError(
                        f"Value '{record.value}' already exists for this Rule and Column combination!"
                    )

    @api.onchange("value")
    def _onchange_value_col(self):
        if self.value and self.column_id and self.deconcat_rule_id and isinstance(self.deconcat_rule_id.id, int):
            domain = [
                ("value", "=", self.value),
                ("deconcat_rule_id", "=", self.deconcat_rule_id.id),
                ("column_id", "=", self.column_id.id),
            ]
            if not isinstance(self.id, int):
                domain.append(("id", "!=", self.id))

            existing = self.search(domain)
            if existing:
                return {
                    "warning": {
                        "title": "Value Already Exists",
                        "message": f"Value '{self.value}' already exists for this Rule and Column combination!",
                    }
                }

# set plan template model
class myndo_set_plan_template(models.Model):
    _name = "myndo.set_plan_template"
    _description = "Myndo Set Template"
    name = fields.Char(string="Name", required=True)
    description = fields.Text(string="Description")
    template_type = fields.Selection([
        ("basic setup", "Basic Setup"),
        ("digital", "Digital"),
        ("offline", "Offline"),
        ("custom", "Custom")
    ], string="Template Type", required=True)
    set_fixed_template = fields.Boolean(string="Set as fixed template", default=False)
    template_related_agency = fields.Many2many("myndo.agency","agency_set_plan_template_rel","set_plan_template_id","agency_id", string="Related Agency")
    
    template_required_columns = fields.One2many("myndo.set_template_columns_usage","template_id",string="Required Columns")
    flowchart_start_column = fields.One2many("myndo.set_template_columns_usage","template_id",string="Flowchart Start Column")
    
    
# downloader template model
class myndo_downloader_template(models.Model):
    _name = "myndo.downloader_template"
    _description = "Myndo Downloader Template"
    name = fields.Char(string="Name", required=True)
    description = fields.Text(string="Description")
    template_type = fields.Selection([
        ("basic setup", "Basic Setup"),
        ("digital", "Digital"),
        ("offline", "Offline"),
        ("custom", "Custom")
    ], string="Template Type", required=True)
    rel_subarea = fields.Many2one("myndo.subarea", string="Subarea")
    rel_client = fields.Many2one("myndo.client", string="Client")
    required_columns = fields.One2many("myndo.downloader_template_columns_usage","template_id",string="Required Columns")
    
    
# myndo cluster
class myndo_cluster(models.Model):
    _name = "myndo.cluster"
    _description = "Myndo Cluster"
    name = fields.Char(string="Name")
    
# validator items
class myndo_cluster_validator_items(models.Model):
    _name = "myndo.cluster_validator_items"
    _description = "Myndo Cluster Validator Items"
    cluster_id = fields.Many2one("myndo.cluster", string="Cluster")
    validator_item = fields.One2many("myndo.validator_items", "cluster_validator_items_id", string="Validator Items")
    
class myndo_validator_items(models.Model):
    _name = "myndo.validator_items"
    _description = "Myndo Validator Items"
    _rec_name = 'accept_values'
    name = fields.Char(string="Name")
    column_id = fields.Many2one("myndo.columns_structure", string="Column")
    cluster_validator_items_id = fields.Many2one("myndo.cluster_validator_items", string="Cluster Validator Items")
    accept_values = fields.Text(string="Accept Values")
    result_values = fields.Text(string="Result Values")
    area_id = fields.Many2many("myndo.area", "validator_items_area_rel", "validator_items_id", "area_id",string="Area")
    
#  save plan records db model
class myndo_planner_templates(models.Model):
	_name='myndo.planner_templates'
	name=fields.Char("Name")
	client=fields.Many2one("myndo.client", string="Client")
	dashboard_user=fields.Many2one("myndo.user_structure", string="Dashboard user")
	is_fixed_template=fields.Boolean("Fixed template")
	definitive=fields.Boolean("definitive")
	is_duplicate = fields.Boolean("is duplicate")
	description=fields.Text("Description")
	client_name=fields.Text("Description")
	date_range=fields.Text("template period")
	brand=fields.Text("Brand")
	country=fields.Text("Country")
	po_number=fields.Text("po number")
	cluster_media=fields.Text("cluster media")
	recurrent_plan=fields.Boolean("recurrent plan")
	is_template_archived=fields.Boolean("is template archived")
	copy_of_plan_id=fields.Integer("copy of plan id")
	convention_rule_id=fields.Integer("convention rule id")
	json_data=fields.Json("data")
	type=fields.Selection(selection=[('basic', 'Basic setup'),('digital', 'Digital'),('offline', 'Offline'),('custom', 'Custom')],string="Scheda")
	columns_totals=fields.Text("columns totals")
class myndo_unicode_list(models.Model):
    _name = "myndo.unicode_list"
    _description = "Myndo Unicode List"
    template_id=fields.Many2one('myndo.planner_templates',string='plan')
    rel_rule_id=fields.Many2one('myndo.deconcat_rules',string='deconcat rule')
    unicode=fields.Char(string='unicode')
    naming_convention=fields.Char(string='naming convention')
    