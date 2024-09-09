from odoo import models, fields, api

class PurchaseOrder(models.Model):
    _inherit = "purchase.order"

    is_consignment_in = fields.Boolean(string="Dépôt Entré")
    consignment_in_state = fields.Selection(
        string="État du Dépôt Entré",
        selection=[
            ("open", "Ouvert"),
            ("closed", "Clôturé")
        ],
        compute='qty_invoiced_changed', store=True
    )
    # @TODO: Think about the return and close scenario

    # @TODO: Should be removed if not used!
    is_received = fields.Boolean(
        string='Has Receipt',
        compute='_compute_is_received',
    )

    @api.onchange('is_consignment_in')
    def _onchange_consignment_in(self):
        print("self:", self)
        print("is_cons_in:", self.is_consignment_in)
        print("\n\n\n\n")
        if self.is_consignment_in:
            self.consignment_in_state = 'open'
        else:
            self.consignment_in_state = False

    @api.depends("order_line.qty_invoiced", 'order_line.return_qty', 'order_line.qty_received')
    def qty_invoiced_changed(self):

        for order in self:

            if order.consignment_in_state != 'open' and not order.order_line:
                if order.consignment_in_state is False and order.is_consignment_in:
                    print("State is changed!!\n\n\n")
                    order.consignment_in_state = 'open'
                continue

            closed = True
            for order_line in order.order_line:
                if order_line.product_qty - order_line.qty_invoiced - order_line.return_qty > 0:
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
