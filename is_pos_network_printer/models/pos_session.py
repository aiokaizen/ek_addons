# -*- coding: utf-8 -*-
from odoo import models


class PosSession(models.Model):

    _name = 'pos.session'
    _inherit = 'pos.session'

    def _loader_params_pos_printer(self):
        return {
            'search_params': {
                'domain': [('id', 'in', self.config_id.printer_ids.ids)],
                'fields': [
                    'name', 'proxy_ip', 'product_categories_ids',
                    'printer_type', 'nw_printer_name'
                ],
            },
        }
