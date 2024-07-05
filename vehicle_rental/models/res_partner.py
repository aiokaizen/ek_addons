from odoo import models, fields, api, _

class Partner(models.Model):
    """Rental Partner"""
    _inherit = 'res.partner'

    paper_ids = fields.One2many('vehicle.rental.partner.paper', 'owner_id', string="Papiers")
    nationality = fields.Char(string=_("nationality"))
    birthday = fields.Date(string=_("Birthday"))