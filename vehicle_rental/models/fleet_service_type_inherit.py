from odoo import fields, models, api
from odoo.addons.http_routing.models.ir_http import slugify


class FleetServiceType(models.Model):

    _inherit = 'fleet.service.type'

    slug = fields.Char(string="Slug")