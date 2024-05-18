# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import fields, models, api


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    pos_iface_network_printer = fields.Boolean(
        related='pos_config_id.iface_network_printer', readonly=False
    )
    pos_printer_name = fields.Char(
        related='pos_config_id.printer_name', readonly=False
    )

    @api.depends('pos_printer_name', 'pos_other_devices')
    def _compute_pos_iface_cashdrawer(self):
        """We are just adding depends on this compute."""
        super()._compute_pos_iface_cashdrawer()

    def _is_cashdrawer_displayed(self, res_config):
        return super()._is_cashdrawer_displayed(res_config) or (
            res_config.pos_other_devices and bool(res_config.pos_printer_name)
        )
