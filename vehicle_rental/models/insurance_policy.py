# -*- coding: utf-8 -*-
# Copyright 2022-Today TechKhedut.
# Part of TechKhedut. See LICENSE file for full copyright and licensing details.
from odoo import fields, models, api, _


class InsurancePolicy(models.Model):
    """Insurance Policy"""
    _name = 'insurance.policy'
    _description = __doc__
    _rec_name = 'policy_number'

    policy_number = fields.Char(string="Policy Number", required=True)
    policy_name = fields.Char(string="Name", required=True)
    description = fields.Char(string="Description")
    file_name = fields.Char(string="File Name")
    avatar = fields.Binary(string="Document")
    policy_amount = fields.Monetary(string="Policy Amount")
    company_id = fields.Many2one('res.company', default=lambda self: self.env.company)
    currency_id = fields.Many2one('res.currency', string='Currency', related="company_id.currency_id")
    vehicle_contract_id = fields.Many2one('vehicle.contract', ondelete="cascade")
