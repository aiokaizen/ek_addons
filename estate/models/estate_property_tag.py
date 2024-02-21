from odoo import fields, models, _


class PropertyTag(models.Model):

    _name = "estate.property.tag"
    _description = _("Property tag")
    _order = "name asc"

    _sql_constraints = [
        (
            'unique_name', 'UNIQUE(name)',
            _('The name should be unique.')
        ),
    ]

    name = fields.Char(
        string="Name", required=True,
        help=_("The name of the real estate property tag."),
    )
    color = fields.Integer(string=_("Color"))
