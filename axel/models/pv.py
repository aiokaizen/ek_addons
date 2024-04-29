from odoo import (
    _, api, fields, models
)
from odoo.addons.axel import settings


class Pv(models.Model):

    _name = "axel.pv"
    _description = _("procès verbal")
    _order = "pv_date desc"

    scanned_pv = fields.Binary(string="P.V Scanné")
    pv_date = fields.Date(_("Date de PV / sinistre"), default=fields.Date.today())
    civilly_responsible = fields.Char(
        _("Civilement responsable")
    )
    license_plate_number = fields.Char(
        _("Matricule")
    )

    def _compute_display_name(self):
        for record in self:
            record.display_name = record.civilly_responsible
