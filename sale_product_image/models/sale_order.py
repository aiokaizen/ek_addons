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


class SaleOrder(models.Model):
    """Inherits the model sale.order"""
    _inherit = 'sale.order'

    is_image_true = fields.Boolean(string="Is Show Image True",
                                   help="Show Image in Sale order Line",
                                   compute="_compute_is_image_true")

    def _compute_is_image_true(self):
        """Method _compute_is_image_true returns True if the Show Image option
        in the sale configuration is true"""
        for rec in self:
            rec.is_image_true = True if rec.env[
                'ir.config_parameter'].sudo().get_param(
                'sale_product_image.is_show_product_image_in_sale_report') else False
