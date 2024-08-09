# -*- coding: utf-8 -*-
# POS Enhancements
# Author: EKBlocks

{
    'name': 'Caisse Master module',
    'version': '1.0',
    'author': 'EKBlocks',
    'category': 'Sales',
    'summary': 'Caisse Master',
    'depends': [
        'point_of_sale',
        'muk_web_colors',
    ],
    'data': [
        # Security
        # 'security/ir.model.access.csv',
    ],
    "assets":  {
        'point_of_sale._assets_pos': [
            'caisse_master/static/src/**/*',
        ],
    },
    'license': 'Other proprietary',
    'application': True,
    "price":  49,
    "currency":  "USD",
}
