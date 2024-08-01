# -*- coding: utf-8 -*-
#############################################################################
#
#    EKBlocks SARL
#
#    Copyright (C) 2024-TODAY EKBlocks (<https://www.ekblocks.com>)
#    Author: MOUAD KOMMIR (k.mouad@ekblocks.com)
#
#############################################################################
from odoo import fields, models


class SaleOrderLine(models.Model):
    """Inherits the model sale.order.line to add a field"""
    _inherit = 'sale.order.line'

    order_line_image = fields.Binary(string="Image",
                                     related="product_id.image_1920",
                                     help='Product Image in Sale orderLine')
