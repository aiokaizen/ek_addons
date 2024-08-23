from odoo import models, fields, api

class PurchaseOrder(models.Model):
    _inherit = "purchase.order"

    is_consignment_in = fields.Boolean(string="Consignement")
    has_receipt = fields.Boolean(
        string='Has Receipt',
        compute='_compute_has_receipt'
    )

    @api.depends('name')
    def _compute_has_receipt(self):
        for order in self:
            # Search for related stock pickings (receipts)
            receipts = self.env['stock.picking'].search([
                ('origin', '=', order.name),
                ('picking_type_id.code', '=', 'incoming'),
                ('state', '!=', 'cancel')  # Optional: Exclude canceled receipts
            ])
            order.has_receipt = bool(receipts)