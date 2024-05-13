# -*- coding: utf-8 -*-
# Custom Real Estate Module
# Author: EKBlocks

{
    'name': 'Axel',
    'version': '1.0',
    'author': 'EKBlocks',
    'category': 'Ekblocks',
    # 'sequence': 15,
    'summary': 'Axel App.',
    'depends': [
        'base',
    ],
    'data': [   
        'security/ir.model.access.csv',
        'data/master_data.xml',
        "views/axel_pv_view.xml",
        "views/axel_expense_view.xml",
        "views/axel_unpaid_view.xml",
        "report/detail_legal_case_template.xml",
        "views/axel_legal_case_view.xml",
        "views/axel_settings_view.xml",
        "report/unpaid_by_client_template.xml",
        # "report/unpaid_by_client_report.xml",
        "views/partner_view.xml",
        "menu/axel_menu.xml"
    ],
    'demo': [
        # 'demo/demo_data.xml',
    ],
    'license': 'LGPL-3',
    'application': True,
}
