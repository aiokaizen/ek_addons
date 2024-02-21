from odoo import fields, models, _


class Users(models.Model):

    _name = "res.users"
    _inherit = "res.users"

    property_ids = fields.One2many(
        "estate.property", "salesman_id",
        domain="[('state', 'in', ['new', 'offer_received'])]",
        string=_("Properties")
    )
