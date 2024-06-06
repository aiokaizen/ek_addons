# -*- coding: utf-8 -*-
# Copyright 2022-Today TechKhedut.
# Part of TechKhedut. See LICENSE file for full copyright and licensing details.
from odoo import models, fields, api, _


class RentalInvoice(models.Model):
    """Rental Invoice"""
    _inherit = 'account.move'
    _description = __doc__

    vehicle_contract_id = fields.Many2one('vehicle.contract', string="Vehicle Contract")


class RentalDeposit(models.Model):
    """Rental Deposit"""
    _inherit = 'account.payment'
    _description = __doc__

    vehicle_contract_id = fields.Many2one('vehicle.contract', string="Vehicle Contract")
