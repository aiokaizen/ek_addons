# -*- coding: utf-8 -*-
# Copyright 2022-Today TechKhedut.
# Part of TechKhedut. See LICENSE file for full copyright and licensing details.
from odoo import models, fields, api, _


class FleetVehicle(models.Model):
    """Fleet Vehicle"""
    _inherit = 'fleet.vehicle'
    _description = __doc__

    rent_day = fields.Monetary(string="Rent / Day")
    rent_week = fields.Monetary(string="Rent / Week")
    rent_month = fields.Monetary(string="Rent / Month")
    rent_km = fields.Monetary(string="Rent / Kilometer")
    rent_mi = fields.Monetary(string="Rent / Mile")

    rent_hour = fields.Monetary(string="Rent / Hour")
    rent_year = fields.Monetary(string="Rent / Year")

    extra_charge_day = fields.Monetary(string="Charge / Day")
    extra_charge_week = fields.Monetary(string="Charge / Week")
    extra_charge_month = fields.Monetary(string="Charge / Month")
    extra_charge_km = fields.Monetary(string="Charge / Kilometer")
    extra_charge_mi = fields.Monetary(string="Charge / Mile")

    extra_charge_hour = fields.Monetary(string="Charge / Hour")
    extra_charge_year = fields.Monetary(string="Charge / Year")

    rental_contract_count = fields.Integer(compute='_total_rental_contract', string=" Contracts")
    status = fields.Selection([('available', 'Operational'), ('in_maintenance', 'Under Maintenance')],
                              string="Status", default="available")

    def available_to_in_maintenance(self):
        self.status = 'in_maintenance'

    def in_maintenance_to_available(self):
        self.status = 'available'

    def _total_rental_contract(self):
        for rec in self:
            rental_contract_count = self.env['vehicle.contract'].search_count([('vehicle_id', '=', rec.id)])
            rec.rental_contract_count = rental_contract_count

    def action_rental_contract_view(self):
        return {
            'type': 'ir.actions.act_window',
            'name': _('Rental Contracts'),
            'res_model': 'vehicle.contract',
            'domain': [('vehicle_id', '=', self.id)],
            'view_mode': 'tree,form,kanban,calendar,pivot,activity',
            'target': 'current',
            'context': {
                'create': False,
            }
        }

    def return_action_to_open(self):
        self.ensure_one()
        xml_id = self.env.context.get('xml_id')
        if xml_id:
            res = self.env['ir.actions.act_window']._for_xml_id('fleet.%s' % xml_id)
            res.update(
                context=dict(self.env.context, default_vehicle_id=self.id, group_by=False),
                domain=[('vehicle_id', '=', self.id)]
            )
            if xml_id == 'fleet_vehicle_log_contract_action':
                res.update(
                    name='Maintenances',
                    display_name='Maintenances'
                )
            return res
        return False

    def action_create_book_contract(self):
        context = self._context
        customer = self.env['res.partner'].browse(context.get('customer_id'))
        data = {
            'vehicle_id': self.id,
            'driver_id': self.driver_id.id,
            'last_odometer': self.odometer,
            'odometer_unit': self.odometer_unit,
            'model_year': self.model_year,
            'transmission': self.transmission,
            'fuel_type': self.fuel_type,
            'license_plate': self.license_plate,
            'customer_id': customer.id,
            'customer_phone': customer.phone,
            'customer_email': customer.email,
            'start_date': context.get('start_date'),
            'end_date': context.get('end_date'),
        }
        vehicle_contract = self.env['vehicle.contract'].sudo().create(data)
        return {
            'type': 'ir.actions.act_window',
            'name': _('Vehicle Contract'),
            'res_model': 'vehicle.contract',
            'res_id': vehicle_contract.id,
            'view_mode': 'form',
            'target': 'current'
        }


class FleetVehicleLogContract(models.Model):
    """Fleet Vehicle Log Contract"""
    _inherit = 'fleet.vehicle.log.contract'
    _description = __doc__

    license_plate = fields.Char(string="License Plate")
