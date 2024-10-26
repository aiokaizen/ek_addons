from odoo import fields, models


class Author(models.Model):
    _name = "librarian.author"
    _description = "librarian.author"

    name = fields.Char(
        "Nom",
        index="btree_not_null",
    )
    is_author = fields.Boolean(default=True)
