# -*- coding: utf-8 -*-
# POS Enhancements
# Author: EKBlocks

{
    'name': 'Insight Sphere POS module',
    'version': '1.0',
    'author': 'EKBlocks',
    'category': 'Sales',
    'summary': 'Insight Sphere POS Enhancements.',
    'depends': [
        'pos_restaurant',
    ],
    'data': [
        # Security
        # 'security/ir.model.access.csv',
        'security/is_restaurant_security.xml',

        # Views
        # 'views/res_partners_views.xml',
    ],
    "assets":  {
        'point_of_sale._assets_pos': [
            'is_restaurant/static/src/**/*',
        ],
    },
    'license': 'Other proprietary',
    'application': True,
    "price":  49,
    "currency":  "USD",
}
