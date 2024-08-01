# -*- coding: utf-8 -*-
#############################################################################
#
#    EKBlocks SARL
#
#    Copyright (C) 2024-TODAY EKBlocks (<https://www.ekblocks.com>)
#    Author: MOUAD KOMMIR (k.mouad@ekblocks.com)
#
#############################################################################
{
    "name": "Sale Order Line Images",
    "version": "17.0.1.0.0",
    "category": 'Sales',
    "summary": "Order Line Images In Sale and Sale Report",
    "description": """Order Line Images In Sale and Sale Report, odoo 17, order line images""",
    'author': 'EKBlocks',
    'company': 'EKBlocks',
    'maintainer': 'EKBlocks',
    "website": "https://www.ekblocks.com",
    "depends": [
        'sale_management',
    ],
    "data": [
        'views/sale_order_line_views.xml',
        'views/res_config_settings_views.xml',
        'report/sale_order_report.xml',
    ],
    # 'images': ['static/description/banner.jpg'],
    'license': 'LGPL-3',
    'installable': True,
    'auto_install': False,
    'application': False,
}
