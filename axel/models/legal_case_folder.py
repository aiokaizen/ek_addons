from odoo import (
    _, api, fields, models
)
from odoo.addons.axel import settings
import logging


_logger = logging.getLogger(__name__)

class LegalCase(models.Model):


    _name = "axel.legal_case"
    _description = _("Axel LegalCase")
    _order = "id desc"

    name = fields.Char(_("Référence"), required=True)
    client_ref = fields.Char(_("Référence client"))
    open_date = fields.Date(
        _("Date d'ouverture"), default=fields.Date.today()
    )
    type = fields.Selection(
        settings.LEGAL_CASE_TYPE_CHOICES,
        string=_("Type de dossier"),
        default="civile"
    )
    court_type = fields.Selection(
        settings.LEGAL_CASE_COURT_TYPE_CHOICES, default="first_instance",
        string=_("Type de tribunal"),
    )
    status = fields.Selection(
        settings.LEGAL_CASE_STATUS_CHOICES, default="pending",
        string=_("État du dossier"),
    )
    court = fields.Char(_("Cour"))
    tribunal = fields.Selection(
        settings.TRIBUNAL_CHOICES,
        string=_("Tribunal"),
    )
    client_id = fields.Many2one(
        "res.partner", string=_("Client"),
        ondelete="restrict", required=True
    )
    pv_id = fields.Many2one(
        "axel.pv", string='PV', required=True
    )
    parent_case_id = fields.Many2one(
        'axel.legal_case', string=_("Dossier parent"))
        
    unpaid = fields.Monetary(
        string=_("Total Impayés"), default=0, compute="_compute_unpaid_legal_case", store=True
    )
    currency_id = fields.Many2one(
        "res.currency", string=_("Currency"), default=lambda self: self.env.ref('base.MAD')
    )
    currency_symbole = fields.Char(
        string=_("Currency Symbol"), compute="_compute_currency_symbole"
    )
    currency_name = fields.Char(
        string=_("Currency name"), compute="_compute_currency_name"
    )
    expense_ids = fields.One2many("axel.expense", "legal_case_id", string="Dépenses")
    payment_ids = fields.One2many("axel.payment", "legal_case_id", string="Recettes")
    charge_ids = fields.One2many("axel.charge", "legal_case_id", string="Honoraires")
    document_ids = fields.One2many("axel.document", "legal_case_id", string="Documents")
    trial_ids = fields.One2many("axel.trial", "legal_case_id", string="Audiences")

    total_expenses = fields.Monetary(
        string="Dépenses total",
        compute="_compute_expense_ids",
    )
    total_payments = fields.Monetary(
        string="Recettes totales",
        compute="_compute_payment_ids",
    )

    total_charges = fields.Monetary(
        string="Honoraire totales",
        compute="_compute_charge_ids",
    )

    total_unpaied = fields.Monetary(
        string="Total impayé",
        compute="_compute_unpaied",
    )

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

    @api.depends("expense_ids")
    def _compute_expense_ids(self):

        for record in self:
            if record.expense_ids:
                total = sum(record.expense_ids.mapped("amount"))
                record.total_expenses = total
            else:
                record.total_expenses = 0
                
    @api.depends("charge_ids")
    def _compute_charge_ids(self):

        for record in self:
            if record.charge_ids:
                total = sum(record.charge_ids.mapped("amount"))
                record.total_charges = total
            else:
                record.total_charges = 0

    @api.depends("payment_ids")
    def _compute_payment_ids(self):
        for record in self:
            if record.payment_ids:
                total = sum(record.payment_ids.mapped("amount"))
                record.total_payments = total
            else:
                record.total_payments = 0
    
    @api.depends("total_expenses", "total_expenses", "total_payments")
    def _compute_unpaied(self):
        for record in self: 
            if record.charge_ids:
                total = record.total_charges + record.total_expenses - record.total_payments
                record.total_unpaied = total
            else:
                record.total_unpaied = 0