# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models


class ResConfigSettings(models.TransientModel):

    _inherit = 'res.config.settings'

    bool_setting1 = fields.Boolean(
        "Lock Confirmed Orders", default=lambda self: self.env.company.po_lock == 'lock'
    )
    bool_setting2 = fields.Boolean(
        "Lock Confirmed 2", default=lambda self: self.env.company.po_lock == 'lock'
    )
