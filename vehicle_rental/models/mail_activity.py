
from odoo import models, fields


class MailActivity(models.Model):

    _inherit = "mail.activity"

    slug = fields.Char(string="Slug", default="")
