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
        'insight_sphere',
        'point_of_sale',
    ],
    'data': [
        'data/master.xml',
        'views/website_template.xml',
        'views/product_views.xml',
    ],
    'demo': [
        'data/demo.xml',
    ],
    "assets":  {
        'point_of_sale._assets_pos': [
            'librarian/static/src/**/*',
        ],
        'web.assets_backend': [
            'librarian/static/src/app/custom_title_service.js',
        ],
    },
    'license': 'Other proprietary',
    'application': True,
    "price":  49,
    "currency":  "USD",
}
