# -*- coding: utf-8 -*-
# E-Commerce implementation for Insight Sphere
# Author: EKBlocks

{
    'name': 'Insight Sphere Chrono Diali Connector',
    'version': '1.0',
    'author': 'EKBlocks',
    'category': 'Tools',
    'summary': 'Insight Sphere Insight Sphere Chrono Diali Connector.',
    'depends': [
        'insight_sphere',
    ],
    'data': [
        'security/ir.model.access.csv',
        'views/is_cd_connector_receiver_views.xml',
        'menus/is_cd_connector_menus.xml',
    ],
    'license': 'Other proprietary',
    'application': True,
}
