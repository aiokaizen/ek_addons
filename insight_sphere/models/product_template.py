from odoo import fields, models, api, _

class ProductTemplate(models.Model):
    _inherit = 'product.template'


    hide_invoice_policy = fields.Boolean(compute="_compute_hide_invoice_policy")

    @api.depends("hide_invoice_policy")
    def _compute_hide_invoice_policy(self):
        for record in self:
            import logging
            _logger = logging.getLogger(__name__)
            _logger.warning("i am in hide invoice policy")
            record.hide_invoice_policy = False 