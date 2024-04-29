from odoo import (
    _, api, fields, models
)
from odoo.addons.axel import settings

class TribunalType(models.Model):

    _name = "axel.tribunal_type"
    _description = _("Type Tribunal")
    _order = "name desc"

    name = fields.Char(_("Nom"))
    sequence = fields.Integer(
        'Sequence', default=1, help=_("Used to order types. Lower is first to appear.")
    )