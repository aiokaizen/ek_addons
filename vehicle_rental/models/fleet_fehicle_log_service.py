from odoo import api, fields, models, _

class FleetVehicleLogServices(models.Model):
    _inherit = 'fleet.vehicle.log.services'

    oil_change_odometer = fields.Integer(_("Vidange kilométrage"), default=10000)
    slug_service = fields.Char("slug", compute="_compute_slug_service",default=lambda self: self._default_slug())

    @api.onchange("service_type_id")
    def _onchange_slug_service(self):
        self.slug_service = self.service_type_id.slug

    @api.model
    def _default_slug(self):
        # Providing a default slug value based on service_type_id, if set
        if self.service_type_id:
            return self.service_type_id.slug
        return ''
    @api.depends("service_type_id")
    def _compute_slug_service(self):
        self.ensure_one()
        self.slug_service = self.service_type_id.slug