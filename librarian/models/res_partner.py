from odoo import models, fields


class ResPartner(models.Model):

    _inherit = 'res.partner'

    is_author = fields.Boolean("Auteur", default=False)
    is_editor = fields.Boolean("Éditeur", default=False)
