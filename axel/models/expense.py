from odoo import (
    _, api, fields, models
)
from odoo.addons.axel import settings


class Expense(models.Model):

    _name = "axel.expense"
    _description = _("Depenses")
    _order = "date desc"

    name = fields.Char(string="Designation")
    amount = fields.Monetary(_("Montant"))
    date = fields.Date(_("Date de dépense"), default=(lambda self : fields.Datetime.now()))
    type = fields.Many2one("axel.expense_type", string=_("Type de dépense"), ondelete="restrict")

    # type_expense = fields.Selection(
    #     settings.EXPENSES_TYPE, _("Type de dépense")
    # )
    legal_case_id = fields.Many2one("axel.legal_case", string=_("Dossier"), ondelete="restrict")
    currency_id = fields.Many2one(
        "res.currency", string=_("Devise"), default=lambda self: self.env.ref('base.MAD')
    )