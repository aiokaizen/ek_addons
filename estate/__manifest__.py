# -*- coding: utf-8 -*-
# Custom Real Estate Module
# Author: EKBlocks

{
    'name': 'Real Estate',
    'version': '1.0',
    'author': 'EKBlocks',
    'category': 'Estate',
    # 'sequence': 15,
    'summary': 'Ads real estate support to Odoo.',
    'depends': [
        'base',
    ],
    'data': [

        'security/ir.model.access.csv',

        'data/master_data.xml',

        'views/estate_property_views.xml',
        'views/estate_property_tag_views.xml',
        'views/estate_property_offer_views.xml',
        'views/estate_property_type_views.xml',
        'views/res_users_views.xml',

        'menus/estate_menus.xml',
    ],
    'demo': [
        'demo/demo_data.xml',
    ],
    'license': 'LGPL-3',
    'application': True,
}
