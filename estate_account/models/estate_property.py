# -*- coding: utf-8 -*-
from datetime import timedelta

from odoo import (
    _, api, fields, models,
    exceptions, Command
)

from odoo.addons.estate.settings import (
    PROPERTY_STATE_CHOICES,
)


class EstateProperty(models.Model):

    _name = "estate.property"
    _inherit = "estate.property"

    state = fields.Selection(
        PROPERTY_STATE_CHOICES, default="new",
        readonly=False
    )
    invoice_id = fields.Many2one('account.move', string=_('Invoice'), readonly=True, copy=False)

    @api.model
    def _get_default_journal(self):
        # Taken from: /addons/account/models/account_bank_statement_line.py
        journal_type = self.env.context.get('journal_type', 'sale')
        return self.env['account.journal'].search([
                *self.env['account.journal']._check_company_domain(self.env.company),
                ('type', '=', journal_type),
            ], limit=1)

    def _prepare_invoice(self):
        """
        Prepare the dict of values to create the new invoice for a sold estate property.
        """
        self.ensure_one()
        journal = self.env['estate.property'].with_context(
            default_move_type='out_invoice',
            journal_type='sale'
        )._get_default_journal()
        if not journal:
            raise exceptions.UserError(
                _(
                    'Please define an accounting sales journal for the company %(name)s (%(id)s).',
                    name=self.buyer_id.name, id=self.buyer_id.id
                )
            )

        today = fields.Date.today()
        invoice_vals = {
            'ref': f"INV-PROPERTY-{self.id}",
            'move_type': 'out_invoice',
            'currency_id': self.currency_id.id,
            'partner_id': self.buyer_id.id,
            'journal_id': journal.id,  # company comes from the journal
            'invoice_date': today,
            'invoice_date_due': today + timedelta(days=30),
            # 'narration': self.note,
            # 'campaign_id': self.campaign_id.id,
            # 'medium_id': self.medium_id.id,
            # 'source_id': self.source_id.id,
            # 'invoice_user_id': self.user_id and self.user_id.id,
            # 'team_id': self.team_id.id,
            # 'partner_shipping_id': self.partner_shipping_id.id,
            # 'fiscal_position_id': (self.fiscal_position_id or self.fiscal_position_id.get_fiscal_position(self.partner_invoice_id.id)).id,
            # 'partner_bank_id': self.company_id.partner_id.bank_ids[:1].id,
            # 'invoice_origin': self.name,
            # 'invoice_payment_term_id': self.payment_term_id.id,
            # 'payment_reference': self.reference,
            # 'transaction_ids': [(6, 0, self.transaction_ids.ids)],
            # 'invoice_line_ids': [],
            # 'company_id': self.company_id.id,
        }
        return invoice_vals

    def sold_property(self):

        self.ensure_one()
        result = super(EstateProperty, self).sold_property()

        # The user can execute this method if they ether have the right to create
        # invoices, or they have the right to create properties.
        if not self.env['account.move'].check_access_rights('create', False):
            try:
                self.check_access_rights('write')
                self.check_access_rule('write')
            except exceptions.AccessError:
                return self.env['account.move']

        # Create invoice
        invoice_vals = self._prepare_invoice()

        # Add invoice lines
        invoice_vals['invoice_line_ids'] = [
            Command.create({
                "name": _("Selling fees"),
                "price_unit": self.selling_price * 0.06,
                "quantity": 1,
            }),
            Command.create({
                "name": _("Administrative fees"),
                "price_unit": 100,
                "quantity": 1,
            })
        ]

        invoice_vals_list = [invoice_vals]
        moves = self.env['account.move'].sudo().with_context(
            default_move_type='out_invoice'
        ).create(invoice_vals_list)
        self.invoice_id = moves.id

        # Send invoice by email or notification?
        # for move in moves:
        #     move.message_post_with_view('mail.message_origin_link',
        #         values={'self': move, 'origin': move.line_ids.mapped('sale_line_ids.order_id')},
        #         subtype_id=self.env.ref('mail.mt_note').id
        #     )

        return result
