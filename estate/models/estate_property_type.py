# -*- coding: utf-8 -*-
from odoo import fields, models, api, _


class PropertyType(models.Model):

    _name = "estate.property.type"
    _description = _("Property type")
    _order = "sequence, name, id"

    _sql_constraints = [
        (
            'unique_name', 'UNIQUE(name)',
            _('The name should be unique.')
        ),
    ]

    name = fields.Char(
        string="Name", required=True,
        help=_("The name of the real estate property type."),
    )
    sequence = fields.Integer(
        'Sequence', default=1, help=_("Used to order types. Lower is first to appear.")
    )
    estate_property_ids = fields.One2many(
        "estate.property",  inverse_name="property_type_id", string=_("Estate properties")
    )
    offer_ids = fields.One2many(
        "estate.property.offer", inverse_name="property_type_id", string=_("Offers")
    )
    offer_count = fields.Integer(string=_("Offer count"), compute="_compute_offer_count")

    @api.depends("offer_ids")
    def _compute_offer_count(self):
        for property_type in self:
            property_type.offer_count = len(property_type.offer_ids)
