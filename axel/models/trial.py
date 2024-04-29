from odoo import (
    _, api, fields, models
)
from odoo.addons.axel import settings

class Trial(models.Model):

    _name = "axel.trial"
    _description = _("Audience")
    _order = "trial_date desc"

    name = fields.Char(_("Nom"), compute="_compute_name")
    amount = fields.Monetary(_("Montant"), required=True)
    trial_date = fields.Date(
        _("Date de demande"), 
        detault=fields.Date.today()
    )
    type = fields.Selection(
        settings.LEGAL_CASE_TYPE_CHOICES, 
        string=_("Type de dossier")
    )
    court_type = fields.Selection(
        settings.LEGAL_CASE_COURT_TYPE_CHOICES, 
        string=_("Type de tribunal"),
        default="first_instance"
    )
    case_number = fields.Char(_("Numéro de dossier"))
    observation = fields.Char(_("Observation"))

    scanned_document = fields.Binary(_("Document Scanné"))
    currency_id = fields.Many2one(
        "res.currency", string=_("Currency"), default=lambda self: self.env.ref('base.MAD')
    )
    legal_case_id = fields.Many2one("axel.legal_case", string=_("Dossier"))

    def _compute_unpaid_legal_case(self):
        for record in self:
            record.unpaid = 0

    @api.depends("amount", "case_number", "legal_case_id")
    def _compute_name(self):
        for record in self:
            record.name = f"{self.legal_case_id.name} {self.case_number}"