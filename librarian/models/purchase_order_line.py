from odoo import api, fields, models, _

class PurchaseOrderLine(models.Model):

    _inherit = 'purchase.order.line'

    counted_qte = fields.Float(string='Quantité restant', compute='_compute_counted_qte')

    # @api.depends()
    def _compute_counted_qte(self):
        current_order = self.order_id
        
        # Get the related stock picking (receipt movement) for the purchase order line
        for rec in self:    
            receipt = self.env['stock.picking'].search([
                ('purchase_id', '=', rec.order_id.id),
                ('purchase_id.is_consignment_in', '=', True),
                ('picking_type_id.code', '=', 'incoming')
            ], order='scheduled_date asc', limit=1)
            counted_qte = 0.0
            if receipt:
                receipt_date = receipt.scheduled_date

                # Get valid sales that were created after the receipt movement
                sales_after_movement = self.env['sale.order'].search([
                    ('state', '=', 'sale'),  # Only consider confirmed sales
                    ('date_order', '>', receipt_date)
                ])

                sales_pos_after_movement = self.env['pos.order'].search([
                    ('state', '=', 'paid'),
                    ('date_order', '>', receipt_date)])
                # Calculate total quantity sold after receipt
                total_qty_sold = sum(
                    sale_line.product_uom_qty
                    for sale in sales_after_movement
                    for sale_line in sale.order_line
                    if sale_line.product_id == rec.product_id
                )

                print(total_qty_sold, ' 0000000000000000000000000000000000000000000000000000000000000')

                total_qty_sold = total_qty_sold + sum(
                    sale_line.qty
                    for sale in sales_pos_after_movement
                    for sale_line in sale.lines
                    if sale_line.product_id == rec.product_id
                )

                print(total_qty_sold, ' 0000000000000000000000000000000000000000000000000000000000000')

                # Find all purchase invoices for this product after the receipt date
                subsequent_invoices = self.env['account.move.line'].search([
                    ('product_id', '=', rec.product_id.id),
                    ('move_id.move_type', '=', 'in_invoice'),  # Only consider purchase invoices
                    ('move_id.state', '=', 'posted'),  # Only posted invoices
                    ('move_id.invoice_date', '>=', receipt_date)  # Invoices after the receipt date
                ])

                # Calculate the total quantity invoiced after the receipt date
                print("loop order:", rec.order_id)
                invoiced_qty_after_receipt = sum(line.quantity for line in subsequent_invoices)
                # if rec.order_id == current_order:
                #     counted_qte = total_qty_sold - invoiced_qty_after_receipt
                # else:
                #     counted_qte = total_qty_sold - invoiced_qty_after_receipt if total_qty_sold - invoiced_qty_after_receipt >= 0 else 0
                invoiced_qty_after_receipt = invoiced_qty_after_receipt - rec.qty_invoiced
                counted_qte = total_qty_sold - invoiced_qty_after_receipt if total_qty_sold - invoiced_qty_after_receipt >= 0 else 0
                counted_qte = counted_qte - rec.qty_invoiced 
                    
            self.counted_qte = counted_qte
