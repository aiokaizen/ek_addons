from odoo import fields, models, api
from odoo.addons.http_routing.models.ir_http import slugify


class FleetServiceType(models.Model):

    _inherit = 'fleet.service.type'

    slug = fields.Char(string="Slug", compute="_compute_slug", store=True)
    
    @api.depends('name')
    def _compute_slug(self):
        for record in self:
            record.slug = slugify(record.name)

    