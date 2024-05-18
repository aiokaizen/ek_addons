from odoo import fields, models, api, _
from odoo.exceptions import ValidationError

class PosPrinter(models.Model):

    _name = 'pos.printer'
    _inherit = 'pos.printer'

    printer_type = fields.Selection(
        string='Printer Type', default='nw_printer',

        # Replace previous selection
        selection=[('nw_printer', 'Use a network printer')]

        # To extend previous selection, we use selection_add instead.
        # selection_add=[('nw_printer', 'Use a network printer')]
    )

    nw_printer_name = fields.Char(
        string='Printer name',
        help="Name of a receipt printer (Same name as in system settings.).", default=""
    )

    @api.constrains('nw_printer_name')
    def _constrains_nw_printer_name(self):
        for record in self:
            if record.printer_type == 'nw_printer' and not record.nw_printer_name:
                raise ValidationError(_("Network printer name cannot be empty."))
