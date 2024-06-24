from datetime import datetime
from odoo import models, fields, api, _
from odoo.addons.http_routing.models.ir_http import slugify


class Type(models.Model):
    """Type Paper"""
    _name = "vehicle.rental.paper.type"
    _description = "Paper types"

    name = fields.Char(string="Name", required=True)
    days_to_alert = fields.Integer("Alerte", default=10)
    sequence = fields.Integer(
        'Sequence', default=1, help=_("Utilisé pour commander des types. Le bas est le premier à apparaître.")
    )
    slug = fields.Char(string="Slug", compute="_compute_slug", store=True)

    @api.depends('name')
    def _compute_slug(self):
        for record in self:
            record.slug = slugify(record.name)
