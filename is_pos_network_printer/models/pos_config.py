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

    iface_network_printer = fields.Boolean(string="Network Printer")
    printer_name = fields.Char(string='Network Printer Name')

class ResConfigSettings(models.TransientModel):
	_inherit = 'res.config.settings'

	pos_iface_network_printer = fields.Boolean(related='pos_config_id.iface_network_printer', readonly=False)
	pos_printer_name = fields.Char(related='pos_config_id.printer_name', readonly=False)
