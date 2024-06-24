# -*- coding: utf-8 -*-
# Copyright 2022-Today TechKhedut.
# Part of TechKhedut. See LICENSE file for full copyright and licensing details.
{
    'name': "Vehicle Rental Management | Car Rent | Car Rental Management",
    'version': "2.0",
    'description': "A car rental, hire car or car hire agency is a company that rents automobiles for short periods.",
    'summary': "Vehicle Rental Management",
    'author': 'TechKhedut Inc.',
    'website': "https://techkhedut.com",
    'depends': ['mail', 'contacts', 'product', 'fleet', 'sale_management', 'bus'],
    'data': [
        # master
        "data/master.xml",
        # data
        'data/vehicle_product_data_views.xml',
        'data/sequence_views.xml',
        'data/vehicle_rental_mail_template.xml',
        'data/report_paper_format.xml',
        'data/ir_cron.xml',
        # Security
        'security/ir.model.access.csv',
        # Wizards
        'wizards/vehicle_damage_views.xml',
        'wizards/rental_contract_booking_views.xml',
        'wizards/return_vehicle_km_view.xml',
        # Views
        'views/assets.xml',
        'views/fleet_inherit_views.xml',
        'views/vehicle_contract_views.xml',
        'views/customer_document_views.xml',
        'views/cancellation_policy_views.xml',
        'views/invoice_inherit_views.xml',
        'views/paper_type_view.xml',
        'views/fleet_vehicle_cost_inherit_views.xml',
        # 'views/fleet_rental_config_view.xml',
        'views/res_config_settings_views.xml',
        # Reports
        'report/vehicle_contract_report_views.xml',
        'report/scratch_report_views.xml',
        # Menus
        'views/menus.xml',
    ],
    'assets': {
        'web.assets_backend': [
            'vehicle_rental/static/src/xml/template.xml',
            'vehicle_rental/static/src/scss/style.scss',
            'vehicle_rental/static/src/js/lib/apexcharts.js',
            'vehicle_rental/static/src/js/lib/moment.min.js',
            'vehicle_rental/static/src/js/dashboard/vehicle_rental_dashboard.js',
        ],
    },
    'images': ['static/description/cover.gif'],
    'license': 'OPL-1',
    'installable': True,
    'application': True,
    'auto_install': False,
    'price': 110,
    'currency': 'EUR',
}
