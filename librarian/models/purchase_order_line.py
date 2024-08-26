from odoo import api, fields, models, _

class PurchaseOrderLine(models.Model):
    _inherit = 'purchase.order.line'

    counted_qte = fields.Float(string='Quantité comptabilisé', compute='_compute_counted_qte')


    @api.depends()
    def _compute_counted_qte(self):
        for rec in self:
            # Get the related stock picking (receipt movement) for the purchase order line
            receipt = self.env['stock.picking'].search([
                ('purchase_id', '=', rec.order_id.id),
                ('purchase_id.is_consignment_in', '=', True),
                ('picking_type_id.code', '=', 'incoming')
            ], order='scheduled_date asc', limit=1)

            if receipt:
                receipt_date = receipt.scheduled_date

                # Get valid sales that were created after the receipt movement
                sales_after_movement = self.env['sale.order'].search([
                    ('state', '=', 'sale'),  # Only consider confirmed sales
                    ('date_order', '>', receipt_date)
                ])
                # Calculate total quantity sold after receipt
                total_qty_sold = sum(
                    sale_line.product_uom_qty
                    for sale in sales_after_movement
                    for sale_line in sale.order_line
                    if sale_line.product_id == rec.product_id
                )


                # Find all purchase invoices for this product after the receipt date
                subsequent_invoices = self.env['account.move.line'].search([
                    ('product_id', '=', rec.product_id.id),
                    ('move_id.move_type', '=', 'in_invoice'),  # Only consider purchase invoices
                    ('move_id.state', '=', 'posted'),  # Only posted invoices
                    ('move_id.invoice_date', '>=', receipt_date)  # Invoices after the receipt date
                ])
                # Calculate the total quantity invoiced after the receipt date
                invoiced_qty_after_receipt = sum(line.quantity for line in subsequent_invoices)
                print('--------------------------------------------------')
                for line in subsequent_invoices:
                    print('subsequent_invoices ', line.quantity , ' invoice id : ', line.move_id.name)
                print('--------------------------------------------------')
                

                # Subtract the invoiced quantity from total quantity sold
                rec.counted_qte = total_qty_sold - invoiced_qty_after_receipt
            else:
                rec.counted_qte = 0.0