# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models
import logging


_logger = logging.getLogger(__name__)


class ResConfigSettings(models.TransientModel):

    _inherit = 'res.config.settings'
    _description = "Insight Sphere main configuration"


    # default_activate_invoincing_policy = fields.Boolean(
    #     default_model="config"
    # )


    activate_invoincing_policy = fields.Boolean(
        "Activate invoicing policy",
        default=False,
        # default=lambda self: self.env['insight_sphere.config'].get_instance().activate_invoincing_policy
    )

    @api.model
    def get_values(self):
        res = super(ResConfigSettings, self).get_values()
        activate_invoincing_policy = self.env['ir.config_parameter'].sudo().get_param('activate_invoincing_policy', False)
        res.update(
            activate_invoincing_policy=activate_invoincing_policy
        )
        return res

    def set_values(self):
        super(ResConfigSettings, self).set_values()
        param_obj = self.env['ir.config_parameter'].sudo()
        param_obj.set_param('activate_invoincing_policy', self.activate_invoincing_policy)
