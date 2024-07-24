# -*- coding: utf-8 -*-
# Insight Sphere Module
# Author: EKBlocks

{
    'name': 'Insight Sphere',
    'version': '2.0',
    'author': 'EKBlocks',
    'category': 'Sales',
    'summary': 'Insight Sphere implementation with Odoo.',
    'depends': [
        'base',
        'account',
        'stock',
        'point_of_sale',
        'sale_management',
        'purchase',

        # Design
        'muk_web_appsbar',
        'muk_web_colors',
    ],
    'data': [
        'security/ir.model.access.csv',
        # 'views/website_template.xml',
        'views/account_move_views.xml',
        'security/ir.model.access.csv',
        'security/insight_sphere_security.xml',

        'views/report_templates.xml',

        'data/master.xml',
        'data/res_company_data.xml',
        'data/report_layout.xml',


        'views/res_config_settings_views.xml',
        'views/product_view.xml',
        'views/website_template.xml',
        'views/insight_sphere_views.xml',
        "views/stock_picking_type_views.xml",

        'menus/insight_sphere_menus.xml',

        'views/report_invoice.xml',

        # 'data/master.xml',
    ],
    'demo': [],
    # 'assets': {
    #     'insight_sphere.assets_backend': [
    #         ('include', 'web._assets_helpers'),
    #         'insight_sphere/static/img/*',
    #         'insight_sphere/static/css/*',
    #         'insight_sphere/static/js/*',
    #     ],
    #     'insight_sphere.assets_web': [
    #         'insight_sphere/static/src/main.js',
    #         'insight_sphere/static/src/start.js',
    #     ],
    # },
    'license': 'Other proprietary',
    'application': True,
}
