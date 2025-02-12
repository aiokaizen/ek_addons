# -*- coding: utf-8 -*-
#################################################################################
#
#   Copyright (c) 2016-Present Webkul Software Pvt. Ltd. (<https://webkul.com/>)
#   See LICENSE file for full copyright and licensing details.
#   License URL : <https://store.webkul.com/license.html/>
#
#################################################################################
from odoo.tools.translate import _
from odoo import api, models
from . escpos import escpos

class PosOrder(models.Model):
    _inherit = 'pos.order'

    @api.model
    def get_esc_command_set(self, data):
        printer = escpos.Escpos()
        printer.receipt(data.get("data"))
        return printer.esc_commands
