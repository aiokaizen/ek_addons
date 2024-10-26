from odoo import fields, models


class Editor(models.Model):
    _name = "librarian.editor"
    _description = "librarian.editor"

    name = fields.Char(
        "Nom",
        index="btree_not_null",
    )
