from odoo import (
    _, api, fields, models
)
from odoo.addons.axel import settings

class Expense(models.Model):

    _name = "axel.expense"
    _description = _("Charges")
    _order = "payment_date desc"

    name = fields.Char(_("Nom"), compute="_compute_name" )
    amount = fields.Monetary(_("Montant"), required=True )
    description = fields.Text(
        _("Description")
        )
    payment_date = fields.Date(_("Date de demande"), detault=fields.Date.today())
    receipt_scanned = fields.Binary(_("Reçu. Scanné"))
    is_paid = fields.Boolean(_("Payé"), default=False)
    currency_id = fields.Many2one(
        "res.currency", string=_("Currency"), default=lambda self: self.env.ref('base.MAD')
    )
    currency_symbole = fields.Char(
        string=_("Currency Symbol"), compute="_compute_currency_symbole"
    )
    currency_name = fields.Char(
        string=_("Currency name"), compute="_compute_currency_name"
    )
    legal_case_id = fields.Many2one("axel.legal_case", string=_("Dossier"))

    @api.depends("amount", "legal_case_id", "payment_date")
    def _compute_name(self):
        for record in self:
            record.name = f"{record.amount} {self.legal_case_id.name} {self.payment_date}"

    
    @api.depends("currency_id")
    def _compute_currency_symbole(self):
        for record in self:
            if record.currency_id:
                record.currency_symbole = record.currency_id.symbol
            else:
                record.currency_symbole = ""

    @api.depends("currency_id")
    def _compute_currency_name(self):
        for record in self:
            if record.currency_id:
                record.currency_name = record.currency_id.name
            else:
                record.currency_name = ""