from odoo import models
from odoo.models import fields


class CODReport(models.Model):

    _name = "cod.report"

    name = fields.Char(string="Name")  # Rapport_start_date_end_date
    file = fields.Binary(string="Rapport")

    def generate_invoices(self):

        product_id = 17  # Use your own product ID

        # Create partners

        # if slugify(partner_id.name) == slugify(client_name):
        #     pass

        # Create Draft Invoices while linking the invoice to the right partner
        pass


class COD(models.Model):

    _name = "cod"

    report_id = fields.Many2one("cod.report", "Rapport")
    delivery_date = fields.Date("Date of Delivery")
    tracking_id = fields.Char("Tracking ID")
    # field_name = fields.Char("Receiver State")
    # field_name = fields.Char("Customer Name")
    # field_name = fields.Char("Customer Contact")
    # field_name = fields.Char("Customer Address")
    # field_name = fields.Char("Customer Postcode")
    # field_name = fields.Char("Granular Status")
    # field_name = fields.Char("Shipper Name")
    # field_name = fields.Char("COD Amount")
    # field_name = fields.Char("COD Fee (Estimate)")
