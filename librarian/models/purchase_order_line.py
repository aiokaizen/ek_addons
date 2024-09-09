from odoo import api, fields, models, _

class PurchaseOrderLine(models.Model):

    _inherit = 'purchase.order.line'

    counted_qte = fields.Float(string='Quantité restante', compute='_compute_counted_qte')

    def _compute_counted_qte(self):
        for rec in self:

            receipt = self.env['stock.picking'].search([
                ('purchase_id', '=', rec.order_id.id),
                ('purchase_id.is_consignment_in', '=', True),
                ('picking_type_id.code', '=', 'incoming'),
                ('state', '=', 'done'),
            ], order='date_done asc', limit=1)

            total_remaining_quantity = 0.0
            if receipt:

                receipt_date = receipt.date_done

                sales_after_movement = self.env['sale.order'].search([
                    ('state', '=', 'sale'),  # Only consider confirmed sales
                    ('date_order', '>', receipt_date)
                ])

                sales_pos_after_movement = self.env['pos.order'].search([
                    ('state', 'in', ['paid', 'done', 'invoiced']),
                    ('date_order', '>', receipt_date)])

                total_qty_sold = sum(
                    sale_line.product_uom_qty
                    for sale in sales_after_movement
                    for sale_line in sale.order_line
                    if sale_line.product_id == rec.product_id
                )

                total_qty_sold = total_qty_sold + sum(
                    sale_line.qty
                    for sale in sales_pos_after_movement
                    for sale_line in sale.lines
                    if sale_line.product_id == rec.product_id
                )

                # Find all purchase invoices for this product after the receipt date
                subsequent_invoices = self.env['account.move.line'].search([
                    ('product_id', '=', rec.product_id.id),
                    ('move_id.move_type', '=', 'in_invoice'),  # Only consider purchase invoices
                    ('move_id.state', '=', 'posted'),
                    # ('move_id.invoice_date', '>=', receipt_date),
                    ('move_id.create_date', '>=', receipt_date),
                ])

                total_supplier_invoiced_qty = sum(line.quantity for line in subsequent_invoices)
                maximum_authorized_to_invoice_qty = rec.product_qty - rec.qty_invoiced
                total_remaining_quantity = total_qty_sold - total_supplier_invoiced_qty
                total_remaining_quantity = max(total_remaining_quantity, 0)
                total_remaining_quantity = min(total_remaining_quantity, maximum_authorized_to_invoice_qty)

            rec.counted_qte = total_remaining_quantity
