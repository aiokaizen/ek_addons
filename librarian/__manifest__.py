# -*- coding: utf-8 -*-
# Librarian
# Author: EKBlocks

{
    'name': 'Librarian',
    'version': '1.0',
    'author': 'EKBlocks',
    'category': 'Sales',
    'summary': 'Librarian',
    'depends': [
        'point_of_sale',
        'muk_web_colors',
    ],
    'data': [
        'views/website_template.xml',
    ],
    "assets":  {
        'point_of_sale._assets_pos': [
            'lirarian/static/src/**/*',
        ],
        'web.assets_backend': [
            'lirarian/static/src/app/custom_title_service.js',
        ],
    },
    'license': 'Other proprietary',
    'application': True,
    "price":  49,
    "currency":  "USD",
}
