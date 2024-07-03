from odoo import api, fields, models
from odoo.addons.vehicle_rental import settings


class FleetVehicleOdometer(models.Model):

    _inherit = 'fleet.vehicle.odometer'
    

    @api.model
    def create(self, vals_list):
        objects = super().create(vals_list)
        IrConfigParam = self.env['ir.config_parameter'].sudo()
        alert_message_km = int(IrConfigParam.get_param('vehicle_rental.alert_message_km', default=1000))
        
        for odometer in objects:
            vehicle = odometer.vehicle_id
            last_vidange = self.env["fleet.vehicle.log.services"].search(
                domain=[
                    ('vehicle_id', '=', vehicle.id),
                    ('service_type_id.slug', '=', 'oil-change'),
                ],
                order='date desc',
                limit=1
            )
            oil_change_odometer = last_vidange.oil_change_odometer or 0
            odometer_at_last_vidange = last_vidange.odometer or 0
            max_odometer_change_oil = int(self.env['ir.config_parameter'].sudo().get_param('rental_vehicle.max_odometer_change_oil', default=10000))
            vidange_lifespan_odometer = oil_change_odometer or max_odometer_change_oil
            odometer_at_last_vidange = last_vidange.odometer if last_vidange else 0
            message = None
            if vehicle.odometer - odometer_at_last_vidange  > vidange_lifespan_odometer:
                message = f"Le véhicule a parcouru plus de {max_odometer_change_oil} km. Il est nécessaire de faire la vidange."
            elif vidange_lifespan_odometer - (vehicle.odometer - odometer_at_last_vidange) <= alert_message_km: # 9000
                message = "Ce véhicule aura bientôt besoin d'une <strong>vidange</strong>."
            if message:
                # TODO: CREATE NEW ACTION
                auto_gen_slug = settings.VEHICLE_ACTIVITIES_AUTOMATIC_CREATION_SLUG

                affected_user = self.env.ref("base.user_admin").id  # User to whome the task is affected.
                vidange_service = self.env["fleet.vehicle.log.services"].search(
                    [
                        ("vehicle_id", '=', vehicle.id),
                        ("service_type_id.slug", "=", 'oil-change')
                    ],
                    order="date desc",
                    limit=1
                )
                vidange_slug = f"{auto_gen_slug}_vidange_{vidange_service.id}" if vidange_service else (
                    f"{auto_gen_slug}_vidange_{vehicle.id}_initial"
                )
                activity_vidange = self.env["mail.activity"].search(
                    domain=[
                        ('slug', '=', vidange_slug)
                    ],
                    limit=1
                )
                if not activity_vidange:
                    vehicle.activity_schedule(
                        'mail.mail_activity_data_todo',  # Activity type (default: To Do)
                        summary="Vidange d'huile nécessaire.",  # Activity title
                        note=message,  # Activity description
                        user_id=affected_user,  # Assign to the current user
                        date_deadline=fields.Date.today(),
                        slug=vidange_slug
                    )

        return objects