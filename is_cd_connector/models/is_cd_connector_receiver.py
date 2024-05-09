from odoo import models
from odoo.models import fields


class Receiver(models.Model):

    _name = "receiver"

    name = fields.Char(
        string="Name",
        default=(lambda self : "API Call " + fields.Datetime.now().strftime("%d/%m/%Y %H:%M"))
    )
    api_url = fields.Char(string="API URL")
    api_data = fields.Json(string="API Data", readonly=True)
    api_data2 = fields.Text(string="API Data")
