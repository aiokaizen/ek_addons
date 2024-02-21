# -*- coding: utf-8 -*-
# Custom Real Estate Accounting Link Module
# Author: EKBlocks

{
    'name': 'Real Estate Accounting link',
    'version': '1.0',
    'author': 'EKBlocks',
    'category': 'Estate',
    'summary': 'A link module between the Real Estate and the Accounting module.',
    'depends': [
        'estate',
        'account',
    ],
    'data': [
        'views/estate_property_views.xml',
    ],
    'license': 'LGPL-3',
    'application': True,
}
