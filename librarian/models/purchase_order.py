from odoo import models, fields, api

class PurchaseOrder(models.Model):
    _inherit = "purchase.order"

    is_consignment_in = fields.Boolean(string="Dépôt Entré")
    consignment_in_state = fields.Selection(
        string="État du Dépôt Entré",
        selection=[
            ("open", "Ouvert"),
            ("closed", "Clôturé"),
            ("returned", "Retourné")
        ],
    )
    # @TODO: Think about the return and close scenario

    # @TODO: Should be removed if not used!
    is_received = fields.Boolean(
        string='Has Receipt',
        compute='_compute_is_received'
    )

    @api.depends("order_line.qty_invoiced")
    def qty_invoiced_changed(self):

        print("\n\n\nqty_invoiced_changed called!\n\n\n")

        for order in self:

            if order.consignment_in_state != 'open':
                continue

            closed = True
            for order_line in order.order_line:
                if order_line.product_qty > order_line.qty_invoiced:
                    closed = False
                    break

            order.consignment_in_state = 'closed' if closed else 'open'

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
