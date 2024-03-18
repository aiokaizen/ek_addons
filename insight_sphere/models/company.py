from odoo import models, fields


class ResCompany(models.Model):
    
    _name = "res.company"
    _inherit = "res.company"

    # chart_template = fields.Selection(
    #     selection='_chart_template_selection',
    #     default="MA",
    # )
    country_id = fields.Many2one(
        'res.country', compute='_compute_address', inverse='_inverse_country', string="Country",
        default="MA"
    )


