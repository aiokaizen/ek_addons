from odoo import models, fields, api

class PurchaseOrder(models.Model):
    _inherit = "purchase.order"

    is_consignment_in = fields.Boolean(string="Dépôt Entré")

    # @TODO: Should be removed if not used!
    is_received = fields.Boolean(
        string='Has Receipt',
        compute='_compute_is_received'
    )

    @api.depends('name')
    def _compute_is_received(self):
        for order in self:
            # Search for related stock pickings (receipts)
            receipts = self.env['stock.picking'].search([
                ('origin', '=', order.name),
                ('picking_type_id.code', '=', 'incoming'),
                ('state', '!=', 'cancel')  # Optional: Exclude canceled receipts
            ])
            order.is_received = bool(receipts)
