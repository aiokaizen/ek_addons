from odoo import (
    _, api, fields, models
)
from odoo.addons.axel import settings

class Payment(models.Model):

    _name = "axel.payment"
    _description = _("Honoraire")
    _order = "payment_date desc"

    name = fields.Char(_("Nom"), compute="_compute_name")
    amount = fields.Monetary(_("Montant"), required=True)
    description = fields.Text(
        _("Description")
    )
    payment_date = fields.Date(_("Date de demande"), detault=fields.Date.today())
    receipt_scanned = fields.Binary(_("Reçu. Scanné"))
    currency_id = fields.Many2one(
        "res.currency", string=_("Currency"), default=lambda self: self.env.ref('base.MAD')
    )
    legal_case_id = fields.Many2one("axel.legal_case", string=_("Dossier"))

    def _compute_unpaid_legal_case(self):
        for record in self:
            record.unpaid = 0

    @api.depends("amount", "legal_case_id")
    def _compute_name(self):
        for record in self:
            record.name = f"{record.amount} {self.legal_case_id.name}"