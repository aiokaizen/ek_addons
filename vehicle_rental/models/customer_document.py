# -*- coding: utf-8 -*-
# Copyright 2022-Today TechKhedut.
# Part of TechKhedut. See LICENSE file for full copyright and licensing details.
from odoo import models, fields, api, _


class CustomerDocument(models.Model):
    """Customer Documents"""
    _name = 'customer.documents'
    _description = __doc__
    _rec_name = 'vehicle_contract_id'

    vehicle_contract_id = fields.Many2one("vehicle.contract", string="Vehicle Contract")
    vehicle_id = fields.Many2one(related='vehicle_contract_id.vehicle_id', string="Vehicle")
    file_name = fields.Char(string="File Name")
    avatar = fields.Binary(string="Document", required=True)
    attachment_ids = fields.Many2many('ir.attachment', string='Attachments')
    delivery_date = fields.Date(string="Délivré (e) le")
    delivery_place = fields.Char(string="Délivré (e) à")
    document_type = fields.Selection([('dl', "Driving license"), ('passport', "Passport"),
                                      ('aadhaar_card', "Aadhaar card"), ('voter_id', "Voter ID card"),
                                      ('ration_card', "Ration card"), ('photo_id', "Photo ID card")],
                                     string="Document Type")
