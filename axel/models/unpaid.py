from odoo import (
    _, api, fields, models
)
from odoo.addons.axel import settings
import logging

_logger = logging.getLogger(__name__)


class Unpaid(models.Model):

    _name = "axel.unpaid"
    _description = _("Impayés")
    _order = "payment_date desc"

    name = fields.Char(_("Nom"), compute="_compute_name" )
    amount = fields.Monetary(_("Montant"), required=True )
    description = fields.Text(
        _("Description")
    )
    payment_date = fields.Date(_("Date de demande"), default=(lambda self : fields.Datetime.now()))
    is_paid = fields.Boolean(_("Payé"), default=False)
    currency_id = fields.Many2one(
        "res.currency", string=_("Devise"), default=lambda self: self.env.ref('base.MAD')
    )
    
    legal_case_id = fields.Many2one("axel.legal_case", string=_("Dossier"))
    client_id = fields.Many2one(
        "res.partner", string=_("Client"),
        ondelete="restrict", required=False, compute="_compute_client_legal_case", readonly=True, store=True
    )   
    receipt_scanned = fields.Binary(_("Reçu. Scanné"))
    type = fields.Selection(
        
        [
            ("expense", _("Dépense")),
            ("charge", _("Honoraire")),
        ],
        string=_("Type"),
        required=True
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
            record.name = f"{record.amount}"