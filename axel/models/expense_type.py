from odoo import (
    _, fields, models
)

class ExpenseType(models.Model):

    _name = "axel.expense_type"
    _description = _("Type de dépense")
    _order = "name desc"

    name = fields.Char(_("Nom") )
    sequence = fields.Integer(
        'Sequence', default=1, help=_("Used to order types. Lower is first to appear.")
    )