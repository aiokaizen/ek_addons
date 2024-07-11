from datetime import datetime
from odoo import models, fields, api, _
from odoo.addons.vehicle_rental import settings


class PaperPartner(models.Model):
    """Paper Vehicule"""
    _name = "vehicle.rental.partner.paper"
    _description = "Paper types"
    # _order = "delivery_date desc"

    _sql_constraints = [
        ('type_owner_unique', 'unique(type, owner_id)', "Chaque propriétaire ne peut avoir qu'un seul type de document. Veuillez vérifier les informations saisies!")
    ]


    type = fields.Selection([('cin', 'CIN'), ('passeport', 'Passeport N'), ('permit', 'Permit')], required=True)
    number = fields.Char(string="Numéro", required=True)
    delivery_date = fields.Date(string="Délivré (e) le")
    delivery_place = fields.Char(string="Délivré (e) à")
    owner_id = fields.Many2one("res.partner", string=_("Propriétaire"))
    attachment_ids = fields.Many2many('ir.attachment', string='Attachments', required=True)