# -*- coding: utf-8 -*-

{
    'name': 'Myndo',
    'summary': "ads module",
    'version': '1.4',
    'author': "Weihao",
    'license': "AGPL-3",
    'maintainer': 'Weihao',
    'category': 'productivity',
    'depends': ['base_setup','web'],
    'data': [
		'views/holding_agency_view.xml',
		'views/agency_view.xml',
		'views/holding_client_view.xml',
		'views/client_view.xml',
		'views/divisions_view.xml',
		'views/columns_view.xml',
		'views/myndo_user_view.xml',
		'views/myndo_area_view.xml',
		'views/subarea_view.xml',
		'views/deconcat_rules_view.xml',
		'views/myndo_set_template_view.xml',
		'views/myndo_platform_view.xml',
		'views/amazon_standardise_column_view.xml',
		'views/validator_items.xml',
		'views/unicode_list_view.xml',
        'views/myndo_menu.xml',
		'security/ir.model.access.csv',
	],
    'auto_install': False,
    'installable': True,
    'application': True,
	# 'assets': {
    #     'web.assets_backend': [
    #         'myndo/static/src/css/myndo-theme.css',
    #     ],
    # },
    # 'assets': {
        # "web.assets_qweb": [
            # 'myndo/templates/*.xml',
        # ],
        # 'web.assets_common': [
            # 'myndo/static/src/css/*',
            
        # ],
        # 'web.assets_common': [
        #     ('prepend', 'myndo/static/src/css/*'),
        # ], 
    # },
}