from datetime import datetime
from odoo import models, fields, api, _


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

    @api.model
    def create(self, vals):
        record = super(Paper, self).create(vals)

        # if record.type_id.slug == "carte-grise":
        #     if not vignette or ((vignette.expiry_date - now.date()).days < days_before_vignette_alert):
        #         next_vignette_date = now.date() if not vignette else vignette.expiry_date
        #         vehicle.activity_schedule(
        #             'mail.mail_activity_data_todo',  # Activity type (default: To Do)
        #             summary="Vignette introuvable.",  # Activity title
        #             note="Vous devez ajouter la vignette pour cette véhicule.",  # Activity description
        #             user_id=self.env.user.id,  # Assign to the current user
        #             date_deadline=next_vignette_date,
        #             slug=auto_gen_slug
        #         )

        return record
