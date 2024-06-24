# rental_vehicle/models/rental_vehicle_config.py

from odoo import models, fields, api, _

class RentalVehicleConfig(models.TransientModel):
    _name = 'rental.vehicle.config'
    _inherit = 'res.config.settings'
    _description = _('Rental Vehicle Settings')

    # max_odometer_change_oil = fields.Integer(string='Max odometer for change oil', default=10000)
    alert_message_km = fields.Integer(string='Alert message before passing odometer', default=9000)
    w18_duration_default = fields.Integer(string='W18 duration default (in months)', default=1)
    recepisse_duration_default = fields.Integer(string='Récépissé duration default (in months)', default=2)
    carte_grise_duration_default = fields.Integer(string='Carte grise default (in years)', default=10)

    # def set_values(self):
    #     super(RentalVehicleConfig, self).set_values()
    #     # self.env['ir.config_parameter'].sudo().set_param('rental_vehicle.max_odometer_change_oil', self.max_odometer_change_oil)
    #     self.env['ir.config_parameter'].sudo().set_param('rental_vehicle.alert_message_km', self.alert_message_km)
    #     self.env['ir.config_parameter'].sudo().set_param('rental_vehicle.w18_duration_default', self.w18_duration_default)
    #     self.env['ir.config_parameter'].sudo().set_param('rental_vehicle.recepisse_duration_default', self.recepisse_duration_default)
    #     self.env['ir.config_parameter'].sudo().set_param('rental_vehicle.carte_grise_duration_default', self.carte_grise_duration_default)

    # @api.model
    # def get_values(self):
    #     res = super(RentalVehicleConfig, self).get_values()
    #     res.update(
    #         # max_odometer_change_oil=int(self.env['ir.config_parameter'].sudo().get_param('rental_vehicle.max_odometer_change_oil', default=10000)),
    #         alert_message_km=int(self.env['ir.config_parameter'].sudo().get_param('rental_vehicle.alert_message_km', default=9000)),
    #         w18_duration_default=int(self.env['ir.config_parameter'].sudo().get_param('rental_vehicle.w18_duration_default', default=1)),
    #         recepisse_duration_default=int(self.env['ir.config_parameter'].sudo().get_param('rental_vehicle.recepisse_duration_default', default=2)),
    #         carte_grise_duration_default=int(self.env['ir.config_parameter'].sudo().get_param('rental_vehicle.carte_grise_duration_default', default=10))
    #     )
    #     return res
