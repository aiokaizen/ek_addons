# -*- coding: utf-8 -*-
# Copyright 2022-Today TechKhedut.
# Part of TechKhedut. See LICENSE file for full copyright and licensing details.
from odoo import fields, api, models, _


class RentalContractBooking(models.TransientModel):
    _name = 'rental.contract.booking'
    _description = "Rental Contract Booking"

    customer_id = fields.Many2one("res.partner", string="Client")
    start_date = fields.Datetime(string="Date de début")
    end_date = fields.Datetime(string="Date de fin")
    fleet_vehicle_ids = fields.Many2many('fleet.vehicle', string="Véhicule")

    @api.onchange('start_date', 'end_date')
    def _onchange_available_vehicle(self):
        if self.start_date and self.end_date:
            rental_contracts = self.env['vehicle.contract'].sudo().search([('start_date', '<=', self.end_date),
                                                                           ('end_date', '>=', self.start_date),
                                                                           ('status', '=', 'b_in_progress'),
                                                                           ('vehicle_id.status', '=', 'available')])
            booked_vehicle_ids = rental_contracts.mapped('vehicle_id').ids
            available_vehicles = self.env['fleet.vehicle'].search([('id', 'not in', booked_vehicle_ids),
                                                                   ('status', '=', 'available')])
            self.fleet_vehicle_ids = [(6, 0, available_vehicles.ids)]
