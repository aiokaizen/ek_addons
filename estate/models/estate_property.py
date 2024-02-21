# -*- coding: utf-8 -*-
from datetime import timedelta

from odoo import (
    _, api, fields, models, exceptions
)
from odoo.tools.float_utils import (
    float_compare
)

from odoo.addons.estate.settings import (
    PROPERTY_STATE_CHOICES,
    PROPERTY_GARDEN_ORIENTATION_CHOICES
)


class EstateProperty(models.Model):

    _name = "estate.property"
    _description = _("Real estate property")
    _order = "id desc"

    _sql_constraints = [
        (
            'check_expected_price', 'CHECK(expected_price >= 0)',
            _('The expected price should be grater than 0.')
        ),
        (
            'check_bedrooms', 'CHECK(bedrooms >= 0)',
            _('The number of bedrooms should be grater than 0.')
        ),
        (
            'check_living_area', 'CHECK(living_area >= 0)',
            _('The living area should be grater than 0.')
        ),
        (
            'check_garden_area', 'CHECK(garden_area >= 0)',
            _('The garden area should be grater than 0.')
        ),
        (
            'check_facades', 'CHECK(facades > 0 AND facades < 5)',
            _('The facades  should be between 1 and 4.')
        ),
    ]

    name = fields.Char(
        string=_("Name"), required=True,  # string: similar to verbose_name in Django
        help=_("The name of the real estate property."),  # help_text in Django
        # index=True  # Requests that Odoo indexes this field in the database.
    )
    description = fields.Text(string=_("Description"))
    postcode = fields.Char(string=_("Postcode"))
    date_availability = fields.Date(
        copy=False, string=_("Date availability"),
        default=(lambda self : fields.Date.today() + timedelta(days=90))
    )
    expected_price = fields.Monetary(required=True, string=_("Expected price"))
    selling_price = fields.Monetary(readonly=True, copy=False, string=_("Selling price"))
    best_price = fields.Monetary(compute="_compute_best_price", string=_("Best offer"))
    currency_id = fields.Many2one(
        "res.currency", string=_("Currency"), default=lambda self: self.env.ref('base.MAD')
    )
    bedrooms = fields.Integer(default=2, string=_("Bedrooms"))
    living_area = fields.Integer(string=_("Living area (sqm)"))
    facades = fields.Integer(string=_("Facades"))
    garage = fields.Boolean(string=_("Garage"))
    garden = fields.Boolean(string=_("Garden"))
    garden_area = fields.Integer(string=_("Garden area (sqm)"))
    garden_orientation = fields.Selection(
        PROPERTY_GARDEN_ORIENTATION_CHOICES,
        string=_("Garden orientation")
    )
    property_type_id = fields.Many2one(
        "estate.property.type", string=_("Property type"),
        ondelete="restrict", required=True
    )
    salesman_id = fields.Many2one(
        "res.users", string=_("Salesman"), copy=False, #  default=lambda self : self._uid,
        ondelete="restrict", readonly=True,
    )
    buyer_id = fields.Many2one(
        "res.partner", string=_("Buyer"), copy=False,
        ondelete="restrict", readonly=True,
    )
    property_tag_ids = fields.Many2many(
        "estate.property.tag", string=_("Tags")
    )
    offer_ids = fields.One2many(
        "estate.property.offer", "property_id", string=_("Offers")
    )

    active = fields.Boolean(default=True, string=_("Active"))
    state = fields.Selection(
        PROPERTY_STATE_CHOICES, default="new", readonly=True,
        string=_("State")
    )

    total_area = fields.Float(
        compute="_compute_total_area", string=_("Total area (sqm)")
    )

    @api.constrains('selling_price')
    def _check_selling_price(self):
        for record in self:
            if float_compare(
                record.selling_price,
                (record.expected_price * 0.9),
                precision_digits=2
            ) == -1:
                raise exceptions.ValidationError(
                    _("The selling price can not be less than 90% of the expected price.")
                )

    @api.depends("living_area", "garden_area")
    def _compute_total_area(self):  # queryset
        for estate_property in self:
            estate_property.total_area = (
                estate_property.living_area + estate_property.garden_area
            )

    @api.depends("offer_ids.price")
    def _compute_best_price(self):
        for estate_property in self:
            if estate_property.offer_ids:
                estate_property.best_price = max(
                    estate_property.offer_ids.mapped("price")
                )
            else:
                estate_property.best_price = 0

    @api.onchange("garden")
    def _onchange_garden(self):
        if self.garden is True:
            self.garden_area = 10
            self.garden_orientation = "north"
        else:
            self.garden_area = 0
            self.garden_orientation = ""
            # return {
            #     'warning': {
            #         'title': _("Warning"),
            #         'message': ('The garden is deactivated. Therefore, garden area and garden orientation were cleared.')
            #     }
            # }

    @api.ondelete(at_uninstall=False)
    def _on_delete(self):
        """
        This method is called before deleting a record by the Odoo framework.
        You can always override the unlink method, but it is not advised.
        """
        for estate_property in self:
            if estate_property.state not in ["new", "canceled"]:
                raise exceptions.UserError(
                    _("Properties that are not new or canceled can not be deleted.")
                )
        return True

    def sold_property(self):
        self.ensure_one()
        if self.state == "canceled":
            raise exceptions.UserError(_("A canceled property can not be sold!"))
        if self.state == "sold":
            return True
        if self.state != 'offer_accepted':
            raise exceptions.UserError(_("You can not sell a property that has no accepted offer."))
        self.state = "sold"
        return {
            'effect': {
                'fadeout': 'slow',
                'message': _("Congratulations! Your property has been sold."),
                'type': 'rainbow_man',
            }
        }

    def cancel_property(self):
        self.ensure_one()
        if self.state == "sold":
            raise exceptions.UserError(_("A sold property can not be canceled!"))
        if self.state == "canceled":
            return True
        self.state = "canceled"
        return True
