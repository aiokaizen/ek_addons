# -*- coding: utf-8 -*-
#################################################################################
#
#   Copyright (c) 2016-Present Webkul Software Pvt. Ltd. (<https://webkul.com/>)
#   See LICENSE file for full copyright and licensing details.
#   License URL : <https://store.webkul.com/license.html/>
#
#################################################################################
from odoo import fields, models
import base64

class PosConfig(models.Model):
    _inherit = 'pos.config'

    network_devices = fields.Boolean(
        string="Network Devices",
        help="Connect devices to your PoS without an IoT Box or Epson printers."
    )
    iface_network_printer = fields.Boolean(string="Network Printer")
    printer_name = fields.Char(string='Network Printer Name')
    qz_server_host = fields.Char(
        string='QZ Tray server host', default="localhost",
        help="Hostname or IP address of the QZ server."
    )

    qz_digital_certificate = fields.Binary(string="Qz digitale certificate")
    qz_private_key = fields.Binary(string="Qz private key")
    base64_qz_digital_certificate = fields.Char(compute="_compute_qz_digital_certificate")


    def _compute_qz_digital_certificate(self):

        for rec in self:
            if rec.qz_digital_certificate:
                rec.base64_qz_digital_certificate = base64.b64decode(rec.qz_digital_certificate)