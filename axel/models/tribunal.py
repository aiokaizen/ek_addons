from odoo import (
    _, api, fields, models
)
from odoo.addons.axel import settings

class Tribunal(models.Model):

    _name = "axel.tribunal"
    _description = _("Tribunal")
    _order = "name desc"

    name = fields.Char(_("Nom") )
    sequence = fields.Integer(
        'Sequence', default=1, help=_("Used to order types. Lower is first to appear.")
    )