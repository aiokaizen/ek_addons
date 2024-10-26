from odoo import models, fields, api


class AccountMoveLine(models.Model):
    _inherit = "account.move.line"

    @api.model
    def create(self, vals):
        if "purchase_line_id" not in vals:
            return super(AccountMoveLine, self).create(vals)
        purchase_line = self.env["purchase.order.line"].browse(vals["purchase_line_id"])

        if "move_id" in vals and purchase_line.order_id.is_consignment_in:
            move = self.env["account.move"].browse(vals["move_id"])
            if move.move_type == "in_invoice":  # Check if it's a purchase invoice
                if (
                    "purchase_line_id" in vals
                ):  # Check if there's a related purchase order line
                    vals["quantity"] = (
                        purchase_line.counted_qte
                    )  # Set the default quantity to 10 or your desired quantity
        return super(AccountMoveLine, self).create(vals)
