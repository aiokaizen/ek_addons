from datetime import timedelta
import logging

from odoo import api, fields, models, exceptions, _

from odoo.addons.estate.settings import (
    PROPERTY_OFFER_STATUS_CHOICES
)


class PropertyOffer(models.Model):

    _name = "estate.property.offer"
    _description = _("Property offer")
    _order = "price desc"

    _sql_constraints = [
        (
            'check_price', 'CHECK(price >= 0)',
            _('The price should be grater than 0.')
        ),
    ]

    price = fields.Monetary(
        string=_("Price"),
        currency_field="currency_id"  # This is the default value
    )
    currency_id = fields.Many2one("res.currency", _("Currency"), default=lambda self: self.env.ref('base.MAD'))
    status = fields.Selection(
        PROPERTY_OFFER_STATUS_CHOICES, copy=False,
        default="pending",
        string=_("Status")
    )

    date_deadline = fields.Date(
        string=_("Deadline"), readonly=False,
        compute="_compute_deadline", inverse="_inverse_deadline",
    )
    validity = fields.Float(default=7, string=_("Validity (Days)"))

    partner_id = fields.Many2one("res.partner", required=True, string=_("Partner"))
    property_id = fields.Many2one("estate.property", required=True, string=_("Property"))
    property_type_id = fields.Many2one(
        "estate.property.type",
        related="property_id.property_type_id",
        string=_("Property type"),
        store=True
    )

    @api.depends("validity")
    def _compute_deadline(self):
        today = fields.Date.today()
        for offer in self:
            start_day = offer.create_date or today
            offer.date_deadline = start_day + timedelta(days=offer.validity)

    def _inverse_deadline(self):
        today = fields.Date.today()
        for offer in self:
            start_day = offer.create_date.date() or today
            offer.validity = (offer.date_deadline - start_day).days

    @api.constrains('date_deadline')
    def _check_deadline(self):
        for record in self:
            if record.date_deadline < fields.Date.today():
                raise exceptions.ValidationError(_("The deadline cannot be set in the past"))

    @api.model
    def create(self, vals):
        # property_id = self.env['estate.property'].browse(vals["property_id"])
        property_id = vals["property_id"]
        property_offers = self.env['estate.property.offer'].search_read(
            [('property_id', '=', property_id)],
            ["price"]
        )
        price_list = [offer['price'] for offer in property_offers]
        if price_list and vals["price"] < max(price_list):
            raise exceptions.UserError(_("You can not add an offer with a lower amount than an existing offer."))

        new_offer = super().create(vals)
        if new_offer.property_id.state == "new":
            new_offer.property_id.state = "offer_received"
        return new_offer

    def accept(self):
        for offer in self:
            if offer.status == "rejected":
                raise exceptions.UserError(_("A rejected offer can not be accepted!"))
            elif offer.status == "accepted":
                return True

            property_id = offer.property_id.id
            accepted_offers = self.env['estate.property.offer'].search_read(
                [('property_id', '=', property_id), ('status', '=', 'accepted')],
            )

            if len(accepted_offers) > 0:
                raise exceptions.UserError(_("Only one offer can be accepted for a given property."))

            offer.status = "accepted"
            offer.property_id.buyer_id = offer.partner_id
            offer.property_id.salesman_id = offer._uid
            offer.property_id.selling_price = offer.price
            offer.property_id.state = "offer_accepted"
            return True

    def reject(self):
        for offer in self:
            if offer.status == "accepted":
                raise exceptions.UserError(_("An accepted offer can not be rejected!"))
            elif offer.status == "rejected":
                return True
            offer.status = "rejected"
