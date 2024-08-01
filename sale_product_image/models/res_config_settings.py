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


class ResConfigSettings(models.TransientModel):
    """Inherits the model res.config.settings to add the field"""
    _inherit = 'res.config.settings'

    is_show_product_image_in_sale_report = fields.Boolean(
        string="Show Product Image",
        config_parameter='sale_product_image.is_show_product_image_in_sale_report',
        help='Show product Image in sale report')
