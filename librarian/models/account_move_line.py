from odoo import models, fields, api

class AccountMoveLine(models.Model):
    _inherit = "account.move.line"



    @api.model
    def create(self, vals):
        if 'move_id' in vals:
            move = self.env['account.move'].browse(vals['move_id'])
            if move.move_type == 'in_invoice':  # Check if it's a purchase invoice
                if 'purchase_line_id' in vals:  # Check if there's a related purchase order line
                    purchase_line = self.env['purchase.order.line'].browse(vals['purchase_line_id'])
                    vals['quantity'] = purchase_line.counted_qte   # Set the default quantity to 10 or your desired quantity
        return super(AccountMoveLine, self).create(vals)