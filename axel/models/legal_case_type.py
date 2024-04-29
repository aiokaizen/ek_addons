from odoo import (
    _, api, fields, models
)
from odoo.addons.axel import settings

class LegalCaseType(models.Model):

    _name = "axel.legal_case_type"
    _description = _("Type de dossier")
    _order = "name desc"

    name = fields.Char(_("Nom") )
    sequence = fields.Integer(
        'Sequence', default=1, help=_("Used to order types. Lower is first to appear.")
    )