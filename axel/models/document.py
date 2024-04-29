from odoo import (
    _, api, fields, models, exceptions
)

class Document(models.Model):

    _name = "axel.document"
    _description = _("Document")
    _order = "name desc"

    name = fields.Char(_("Nature du document"), required=True, default="")
    document_file = fields.Binary(_("Fichier"))
    legal_case_id = fields.Many2one("axel.legal_case", string=_("Dossier"))
