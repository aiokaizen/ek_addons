from odoo import fields, models, _, api
import logging
_logger = logging.getLogger(__name__)

class ResPartner(models.Model):
    _name = 'res.partner'
    _inherit = 'res.partner'

    expense_ids = fields.One2many(
        'axel.expense',
        'client_id',
        string='Expenses',
        compute="_compute_expense_ids",
        readonly=True,
        store=True
    )
    charge_ids = fields.One2many(
        'axel.charge',
        'client_id',
        string='Charge',
        compute="_compute_charge_ids",
        readonly=True,
        store=True
    )
    total_unpaid = fields.Monetary(compute="_compute_total_unpaid", string=_("Montant"), )
    legal_case_ids = fields.One2many(
        'axel.legal_case', 'client_id', string='Legal Cases', readonly=True,
        required=False
    )
    currency_id = fields.Many2one(
        "res.currency", string=_("Currency"), default=lambda self: self.env.ref('base.MAD')
    )

    @api.depends("legal_case_ids")
    def _compute_expense_ids(self):
        # self.ensure_one()
        # for record in self:
        expenses = self.env["axel.expense"].search([
        ("legal_case_id", "in", self.legal_case_ids._ids), 
        ("is_paid", "=", False), 
        
        ])

        self.expenses_ids = expenses

    @api.depends("legal_case_ids")
    def _compute_charge_ids(self):
        # self.ensure_one()
        # for record in self:
        charges = self.env["axel.charge"].search([
        ("legal_case_id", "in", self.legal_case_ids._ids), 
        ("is_paid", "=", False), 
        
        ])
        self.expenses_ids = charges

    @api.depends("currency_id")
    def _compute_total_unpaid(self):
        self.ensure_one()
        # for record in self:
        # _logger.warning(self.expenses)
        total_expenses = sum(self.expenses.mapped("amount"))
        total_charges = sum(self.charges.mapped("amount"))
        self.total_unpaid = total_expenses + total_charges 

    # Define property expenses of a client without save them in db
    @property
    def expenses(self):
        expenses = self.env["axel.expense"].search([
            ("legal_case_id", "in", self.legal_case_ids._ids), 
            ("is_paid", "=", False), 
            
        ])
        return expenses

    # Honoraires
    @property
    def charges(self):
        charges = self.env["axel.charge"].search([
            ("legal_case_id", "in", self.legal_case_ids._ids),
            ("is_paid", "=", False), 
        ])
        return charges

    def print_unpaid_by_client(self):
        self.ensure_one()
        # domain_expenses = [
        #     ("legal_case_id", "in", self.legal_case_ids._ids),
        #     ("is_paid", "=", False), 
        # ]
        return {
            'type': 'ir.actions.act_window',
            'name': _("La liste des impayés"),
            'res_model': 'res.partner',
            'view_mode': 'form',
            'domain': [],
            'views': [(self.env.ref('axel.axel_unpaid_form').id, 'form'), (False, 'tree')],
        }
    
