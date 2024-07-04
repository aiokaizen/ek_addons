from datetime import datetime
from odoo import models, fields, api, _
from odoo.addons.vehicle_rental import settings


class PaperPartner(models.Model):
    """Paper Vehicule"""
    _name = "vehicle.rental.partner.paper"
    _description = "Paper types"
    # _order = "delivery_date desc"

    type = fields.Selection([('cin', 'CIN'), ('passeport', 'Passeport N'), ('permit', 'Permit')])
    delivery_date = fields.Date(string="Délivré (e) le")
    delivery_place = fields.Char(string="Délivré (e) à")
    owner_id = fields.Many2one("res.partner", string=_("Propriétaire"))
    file = fields.Binary(
        attachment=True,
        string="Document",
        copy=False,
    )
    attachment_ids = fields.Many2many('ir.attachment', string='Attachments')
    filename = fields.Char('File Name')
