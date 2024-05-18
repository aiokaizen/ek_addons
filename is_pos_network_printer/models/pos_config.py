# -*- coding: utf-8 -*-
#################################################################################
#
#   Copyright (c) 2016-Present Webkul Software Pvt. Ltd. (<https://webkul.com/>)
#   See LICENSE file for full copyright and licensing details.
#   License URL : <https://store.webkul.com/license.html/>
#
#################################################################################
from odoo import fields, models

class PosConfig(models.Model):
    _inherit = 'pos.config'

    network_devices = fields.Boolean(
        string="Network Devices",
        help="Connect devices to your PoS without an IoT Box or Epson printers."
    )
    iface_network_printer = fields.Boolean(string="Network Printer")
    printer_name = fields.Char(string='Network Printer Name')
