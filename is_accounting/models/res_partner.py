from odoo import fields, models, _


class Partner(models.Model):

    _name = "res.partner"
    _inherit = "res.partner"

    ice = fields.Char(string="ICE")
    rc = fields.Char(string="RC")
