from odoo import (
    _, api, fields, models, exceptions
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
        _("Date d'ouverture"), default=(lambda self : fields.Datetime.now())
    )
    
    type = fields.Many2one("axel.legal_case_type", string=_("Type de dossier"), ondelete="restrict")
  
    court_type = fields.Many2one("axel.tribunal_type", string=_("Type de tribunal"), ondelete="restrict")
    status = fields.Selection(
        settings.LEGAL_CASE_STATUS_CHOICES, default="pending",
        string=_("État du dossier"),
    )
    court = fields.Char(_("Cour"))
   
    tribunal = fields.Many2one("axel.tribunal", string=_("Tribunal"), ondelete="restrict")
    client_id = fields.Many2one(
        "res.partner", string=_("Client"),
        ondelete="restrict", required=True
    )
    pv_id = fields.Many2one(
        "axel.pv", string='PV', required=True
    )
    parent_case_id = fields.Many2one(
        'axel.legal_case', string=_("Dossier parent")
    )
    
   
    currency_id = fields.Many2one(
        "res.currency", string=_("Devise"), default=lambda self: self.env.ref('base.MAD')
    )

    expense_ids = fields.One2many(
        "axel.unpaid", 
        "legal_case_id", 
        string="Depenses", 
        domain=[("type", "=", "expense")],
    )
    charge_ids = fields.One2many(
        "axel.unpaid", 
        "legal_case_id", 
        string="Honoraires", 
        domain=[("type", "=", "charge")],
    )

    payment_ids = fields.One2many("axel.payment", "legal_case_id", string="Recettes")
    document_ids = fields.One2many("axel.document", "legal_case_id", string="Documents")
    trial_ids = fields.One2many("axel.trial", "legal_case_id", string="Audiences")

    total_expenses = fields.Monetary(
        string="Dépenses total",
        compute="_compute_total_expenses",
    )
    total_payments = fields.Monetary(
        string="Recettes totales",
        compute="_compute_payment_ids",

    )

    total_charges = fields.Monetary(
        string="Honoraire totales",
        compute="_compute_total_charges",
    )

    total_unpaied = fields.Monetary(
        string="Total impayé",
        compute="_compute_unpaied",
        store=True
    )



    @api.depends("expense_ids")
    def _compute_total_expenses(self):
        for record in self:
            if record.expense_ids:
                total = sum(record.expense_ids.mapped("amount"))
                record.total_expenses = total
            else:
                record.total_expenses = 0
                
    @api.depends("charge_ids")
    def _compute_total_charges(self):

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

    @api.depends("total_unpaied")
    def mark_as_paid(self):
        self.ensure_one()
        if self.total_unpaied > 0:
            raise exceptions.UserError(_("Impossible de marquer ce dossier comme payé. Veuillez régler tout paiement impayé avant de le marquer comme payé."))
        else:
            self.status = "paied"

    
    @api.depends("total_unpaied")
    def mark_as_pending(self):
        self.ensure_one()
        self.status = "pending"

    
    @api.depends("total_unpaied")
    def mark_as_archived(self):
        self.ensure_one()
        self.status = "archived"


    
    def get_report_values(self, docids, data=None):
        docs = self.env['axel.legal_case'].browse(docids)
        # Retrieve the current company's information
        current_company = self.env.company
        # Add company information to the context
        report_context = {
            'docs': docs,
            'current_company': current_company,
        }
        return report_context

    def get_current_company(self):
        return [self.env.company.primary_color, self.env.company.secondary_color]
    
    def _get_report_from_name(self):
        self.ensure_one()
        return "dossier_" + self.name