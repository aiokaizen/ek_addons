from odoo import fields, models, _, api
import logging
_logger = logging.getLogger(__name__)

class ResPartner(models.Model):
    _name = 'res.partner'
    _inherit = 'res.partner'

    legal_case_ids = fields.One2many(
        'axel.legal_case', 'client_id', string='Legal Cases', readonly=True,
        required=False
    )


    # Define
    @property
    def expenses(self):
        LegalCase = self.env['axel.legal_case']

        legal_case_ids = LegalCase.search([('client_id', '=', self.id)])
        expenses = self.env["axel.expense"].search([("legal_case_id", "in", legal_case_ids._ids)])
        return expenses



    def print_unpaid_by_client(self):
        self.ensure_one()
        LegalCase = self.env['axel.legal_case']

        legal_case_ids = LegalCase.search([('client_id', '=', self.id)])
        domain_expenses = [("legal_case_id", "in", legal_case_ids._ids)]
        action = self.env['ir.actions.act_window'].create({
            'name': 'Unpaid Legal Cases',
            'type': 'ir.actions.act_window',
            'res_model': 'axel.expense',
            'view_mode': 'tree',
            'domain': domain_expenses,
            'context': {}
        })
        return {
            'type': 'ir.actions.act_window',
            'res_model': 'ir.actions.act_window',
            'view_mode': 'tree',
            'res_id': action.id,
            'target': 'current',
        }
