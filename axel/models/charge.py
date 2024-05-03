from odoo import (
    _, api, fields, models
)
from odoo.addons.axel import settings

class Charge(models.Model):

    _name = "axel.charge"
    _description = _("Honoraire")
    _order = "payment_date desc"

    name = fields.Char(_("Nom"), compute="_compute_name" )
    amount = fields.Monetary(_("Montant"), required=True )
    description = fields.Text(
        _("Description")
    )
    payment_date = fields.Date(_("Date de demande"), detault=fields.Date.today())
    is_paid = fields.Boolean(_("Payé"), default=False)
    currency_id = fields.Many2one(
        "res.currency", string=_("Currency"), default=lambda self: self.env.ref('base.MAD')
    )
    currency_symbole = fields.Char(
        string=_("Currency Symbol"), compute="_compute_currency_symbole"
    )
    legal_case_id = fields.Many2one("axel.legal_case", string=_("Dossier"))
    client_id = fields.Many2one(
        "res.partner", string=_("Client"),
        ondelete="restrict", required=False, compute="_compute_client_legal_case", readonly=True, store=True
    )

    @api.depends("legal_case_id")
    def _compute_client_legal_case(self):
        for record in self:
            record.client_id = record.legal_case_id.client_id

    def _compute_unpaid_legal_case(self):
        for record in self:
            record.unpaid = 0

    @api.depends("amount", "legal_case_id")
    def _compute_name(self):
        for record in self:
            record.name = f"{record.amount} {record.legal_case_id.name}"


    @api.depends("currency_id")
    def _compute_currency_symbole(self):
        for record in self:
            if record.currency_id:
                record.currency_symbole = record.currency_id.symbol
            else:
                record.currency_symbole = ""