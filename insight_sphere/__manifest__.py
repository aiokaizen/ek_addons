# -*- coding: utf-8 -*-
# Insight Sphere Module
# Author: EKBlocks

{
    'name': 'Insight Sphere',
    'version': '2.0',
    'author': 'EKBlocks',
    'category': 'Sales',
    'summary': 'Insight Sphere implementation in Odoo.',
    'depends': [
        'stock',
        'account',
        'point_of_sale',
        'sale_management',
        'purchase',

        # Design
        'muk_web_colors',
    ],
    'data': [
        # 'security/ir.model.access.csv',
        'menus/insight_sphere_menus.xml',
        'views/website_template.xml',
        # 'data/master.xml',
        # 'views/res_config_settings_views.xml',
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
