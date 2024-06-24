# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import models, fields, api, _



class ResConfigSettings(models.TransientModel):
    _inherit = ['res.config.settings']

    alert_message_km = fields.Integer(string='Alert message before passing odometer', default=1000)
    w18_duration_default = fields.Integer(string='W18 duration default (in months)', default=1)
    recepisse_duration_default = fields.Integer(string='Récépissé duration default (in months)', default=1)
    carte_grise_duration_default = fields.Integer(string='Carte grise default (in years)', default=10)
    

    @api.model
    def get_values(self):
        res = super(ResConfigSettings, self).get_values()
        IrConfigParam = self.env['ir.config_parameter'].sudo()
        res.update(
            alert_message_km=int(IrConfigParam.get_param('vehicle_rental.alert_message_km', default=1000)),
            w18_duration_default=int(IrConfigParam.get_param('vehicle_rental.w18_duration_default', default=1)),
            recepisse_duration_default=int(IrConfigParam.get_param('vehicle_rental.recepisse_duration_default', default=1)),
            carte_grise_duration_default=int(IrConfigParam.get_param('vehicle_rental.carte_grise_duration_default', default=10)),
        )
        return res

    def set_values(self):
        super(ResConfigSettings, self).set_values()
        IrConfigParam = self.env['ir.config_parameter'].sudo()
        IrConfigParam.set_param('vehicle_rental.alert_message_km', self.alert_message_km)
        IrConfigParam.set_param('vehicle_rental.w18_duration_default', self.w18_duration_default)
        IrConfigParam.set_param('vehicle_rental.recepisse_duration_default', self.recepisse_duration_default)
        IrConfigParam.set_param('vehicle_rental.carte_grise_duration_default', self.carte_grise_duration_default)