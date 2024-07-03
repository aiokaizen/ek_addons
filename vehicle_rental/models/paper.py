from datetime import datetime
from odoo import models, fields, api, _
from odoo.addons.vehicle_rental import settings


class Paper(models.Model):
    """Paper Vehicule"""
    _name = "vehicle.rental.paper"
    _description = "Paper types"
    _order = "issue_date desc"

    type_id = fields.Many2one("vehicle.rental.paper.type", string=_("Types"), required=True)
    issue_date = fields.Date(string=_("Date Début"), required=True)
    expiry_date = fields.Date(string=_("Date Fin"), required=True)
    owner_id = fields.Many2one("res.partner", string=_("Propriétaire"))
    vehicle_id = fields.Many2one("fleet.vehicle", required=True, string=_("Véhicule"))
    odometer = fields.Float(string=_("Odometer"), copy=False)
    file = fields.Binary(
        attachment=True,
        string="Document",
        copy=False,
    )
    filename = fields.Char('File Name')

    @api.model
    def create(self, vals):
        record = super(Paper, self).create(vals)
        auto_gen_slug = settings.VEHICLE_ACTIVITIES_AUTOMATIC_CREATION_SLUG

        vignette = self.vehicle_id.paper_ids.filtered(
            lambda p: p.type_id.slug == "vignette"
        ).search([], limit=1)

        if record.type_id.slug == "carte-grise" and not vignette:

            vignette_slug = f"{auto_gen_slug}_vignette_initial"

            self.vehicle_id.activity_schedule(
                'mail.mail_activity_data_todo',  # Activity type (default: To Do)
                summary="Vignette introuvable.",  # Activity title
                note="Vous devez ajouter la vignette pour cette véhicule.",  # Activity description
                user_id=self.env.user.id,  # Assign to the current user
                slug=vignette_slug
            )

        return record
