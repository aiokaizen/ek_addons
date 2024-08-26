# -*- coding: utf-8 -*-
# POS Enhancements
# Author: EKBlocks

{
    'name': 'Caisse Master Restaurant module',
    'version': '1.0',
    'author': 'EKBlocks',
    'category': 'Sales',
    'summary': 'Caisse Master Restaurant',
    'depends': [
        'caisse_master',
        'pos_restaurant',
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
