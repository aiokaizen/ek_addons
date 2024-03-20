from odoo import models


class AccountMove(models.Model):

    _inherit = "account.move"

    def _get_name_invoice_report(self):
        """ This method need to be inherit by the localizations if they want to print a custom invoice report instead of
        the default one. For example please review the l10n_ar module """
        self.ensure_one()
        return 'insight_sphere.report_invoice_document'
