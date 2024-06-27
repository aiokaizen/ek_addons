# -*- coding: utf-8 -*-
# Copyright 2022-Today TechKhedut.
# Part of TechKhedut. See LICENSE file for full copyright and licensing details.
from datetime import timedelta
from odoo import models, fields, api, _
from dateutil.relativedelta import relativedelta
import logging
from markupsafe import Markup

from odoo.addons.vehicle_rental import settings

_logger = logging.getLogger(__name__)

class FleetVehicle(models.Model):
    """Fleet Vehicle"""
    _inherit = 'fleet.vehicle'
    _description = __doc__

    rent_day = fields.Monetary(string="Rent / Day")
    rent_week = fields.Monetary(string="Rent / Week")
    rent_month = fields.Monetary(string="Rent / Month")
    rent_km = fields.Monetary(string="Rent / Kilometer")
    rent_mi = fields.Monetary(string="Rent / Mile")

    rent_hour = fields.Monetary(string="Rent / Hour")
    rent_year = fields.Monetary(string="Rent / Year")

    extra_charge_day = fields.Monetary(string="Charge / Day")
    extra_charge_week = fields.Monetary(string="Charge / Week")
    extra_charge_month = fields.Monetary(string="Charge / Month")
    extra_charge_km = fields.Monetary(string="Charge / Kilometer")
    extra_charge_mi = fields.Monetary(string="Charge / Mile")

    extra_charge_hour = fields.Monetary(string="Charge / Hour")
    extra_charge_year = fields.Monetary(string="Charge / Year")

    rental_contract_count = fields.Integer(compute='_total_rental_contract', string=" Contracts")
    status = fields.Selection([('available', 'Operational'), ('in_maintenance', 'Under Maintenance')],
                              string="Status", default="available")
    paper_ids = fields.One2many("vehicle.rental.paper", "vehicle_id", string="Papiers")

    has_alert_message = fields.Html(compute="_compute_has_alert")


    def available_to_in_maintenance(self):
        self.status = 'in_maintenance'

    def in_maintenance_to_available(self):
        self.status = 'available'

    def _total_rental_contract(self):
        for rec in self:
            rental_contract_count = self.env['vehicle.contract'].search_count([('vehicle_id', '=', rec.id)])
            rec.rental_contract_count = rental_contract_count

    def action_rental_contract_view(self):
        return {
            'type': 'ir.actions.act_window',
            'name': _('Rental Contracts'),
            'res_model': 'vehicle.contract',
            'domain': [('vehicle_id', '=', self.id)],
            'view_mode': 'tree,form,kanban,calendar,pivot,activity',
            'target': 'current',
            'context': {
                'create': False,
            }
        }

    def return_action_to_open(self):
        self.ensure_one()
        xml_id = self.env.context.get('xml_id')
        if xml_id:
            res = self.env['ir.actions.act_window']._for_xml_id('fleet.%s' % xml_id)
            res.update(
                context=dict(self.env.context, default_vehicle_id=self.id, group_by=False),
                domain=[('vehicle_id', '=', self.id)]
            )
            if xml_id == 'fleet_vehicle_log_contract_action':
                res.update(
                    name='Maintenances',
                    display_name='Maintenances'
                )
            return res
        return False

    def action_create_book_contract(self):
        context = self._context
        customer = self.env['res.partner'].browse(context.get('customer_id'))
        data = {
            'vehicle_id': self.id,
            'driver_id': self.driver_id.id,
            'last_odometer': self.odometer,
            'odometer_unit': self.odometer_unit,
            'model_year': self.model_year,
            'transmission': self.transmission,
            'fuel_type': self.fuel_type,
            'license_plate': self.license_plate,
            'customer_id': customer.id,
            'customer_phone': customer.phone,
            'customer_email': customer.email,
            'start_date': context.get('start_date'),
            'end_date': context.get('end_date'),
        }
        vehicle_contract = self.env['vehicle.contract'].sudo().create(data)
        return {
            'type': 'ir.actions.act_window',
            'name': _('Vehicle Contract'),
            'res_model': 'vehicle.contract',
            'res_id': vehicle_contract.id,
            'view_mode': 'form',
            'target': 'current'
        }


    def _check_number_of_month_by_acquisition_date(record, number_of_month):
        current_date = fields.Datetime.now().date()
        x_month_later = record.acquisition_date + relativedelta(months=number_of_month)
        if current_date > x_month_later:
            return True
        return False



    def _get_paper_by_slug(self, slug):
        return self.env["vehicle.rental.paper"].search(
            domain=[
                ('vehicle_id', '=', self.id),
                ('type_id.slug', '=', slug)
            ],
            order='create_date desc',
            limit=1
        )

    def _add_msg_to_alert(self, slug, missing_msg, expiring_soon_msg, expired_msg):
        paper = self._get_paper_by_slug(slug)
        current_date = fields.Datetime.now().date()

        if not paper and missing_msg:
            return (missing_msg, 'danger')
        if not paper:
            return False
        diff_days = (paper.expiry_date - current_date).days
        if paper.type_id.days_to_alert >= diff_days and diff_days > 0:
            return (expiring_soon_msg, 'warning')
        elif current_date > paper.expiry_date:

            return (expired_msg, 'danger')
        else:
            return False

#     def create_cron_job(self):
#         now = fields.Datetime.now()
#         for vehicle in self:
#             print("TESTTTTTTTTTTTTTTTTTTTTTTTTTTTTTT", vehicle.name)

#             self.env["ir.cron"].create({
#                 "name": "Test cron created by code for fleet vehicle!",
#                 "model_id": self.env["ir.model"].search([("model", "=", "fleet.vehicle")], limit=1).id,
#                 "interval_type": "hours",
#                 "interval_number": 24,
#                 "numbercall": 3,
#                 "active": True,
#                 # "nextcall": vehicle.acquisition_date + timedelta(days=30),
#                 "nextcall": now + timedelta(seconds=10),
#                 "help": "This is a test cron that was created automatically (Inactive by default)!!!",
#                 # "groups_id": [self.env.ref('base.group_system').id,],
#                 "groups_id": [],
#                 "priority": 4,
#                 # "ir_actions_server_id": self.env.ref('actions.some_action').id,
#                 "code": """
# vehicle = env["fleet.vehicle"].search([], limit=1)
# vehicle.check_vehicle_tasks()
# _logger.info("Hello there!!!")
#                 """,
#             })
#         return True

    def create_vehicle_papers_tasks(self):
        """
        This function creates the tasks related to the vehicle papers if they do not already exist.
        It is called from a cron job and other places.
        """
        now = fields.Datetime.now()
        for vehicle in self:
            # print("TEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEST", vehicle.name)
            # vehicle.activity_schedule(
            #     'mail.mail_activity_data_todo',  # Activity type (default: To Do)
            #     summary="Carte grise introuvable.",  # Activity title
            #     note="Vous devez ajouter une Carte Grise pour cette véhicule.",  # Activity description
            #     user_id=vehicle.env.user.id,  # Assign to the current user
            #     # date_deadline=vehicle.acquisition_date + timedelta(days=60),
            # )
            # print("FIIIIIIIIIIIIIIIIIIIIN   TEEEEEEEEEEEEEEEEEEEEEEEEST")
            # continue

            IrConfigParam = self.env['ir.config_parameter'].sudo()
            auto_gen_slug = settings.VEHICLE_ACTIVITIES_AUTOMATIC_CREATION_SLUG

            days_before_carte_grise_alert = self.env['vehicle.rental.paper.type'].search(
                [("slug", "=", "carte-grise")], limit=1
            ).days_to_alert
            carte_grise = vehicle.paper_ids.filtered(
                lambda p: p.type_id.slug == "carte-grise"
            ).search([], limit=1)

            days_before_visite_technique_alert = self.env['vehicle.rental.paper.type'].search(
                [("slug", "=", "visite-technique")], limit=1
            ).days_to_alert
            visite_technique = vehicle.paper_ids.filtered(
                lambda p: p.type_id.slug == "visite-technique"
            ).search([], limit=1)

            days_before_vignette_alert = self.env['vehicle.rental.paper.type'].search(
                [("slug", "=", "vignette")], limit=1
            ).days_to_alert
            vignette = vehicle.paper_ids.filtered(
                lambda p: p.type_id.slug == "vignette"
            ).search([], limit=1)

            days_before_assurance_alert = self.env['vehicle.rental.paper.type'].search(
                [("slug", "=", "assurance")], limit=1
            ).days_to_alert
            assurance = vehicle.paper_ids.filtered(
                lambda p: p.type_id.slug == "assurance"
            ).search([], limit=1)

            if vehicle.acquisition_date:

                carte_grise_activity_slug = f"{auto_gen_slug}_carte_grise_{carte_grise.id}" if carte_grise else (
                    f"{auto_gen_slug}_carte_grise_initial"
                )

                if not carte_grise or ((carte_grise.expiry_date - now.date()).days < days_before_carte_grise_alert):
                    vehicle.activity_schedule(
                        'mail.mail_activity_data_todo',  # Activity type (default: To Do)
                        summary="Carte grise introuvable.",  # Activity title
                        note="Vous devez ajouter une Carte Grise pour cette véhicule.",  # Activity description
                        user_id=self.env.user.id,  # Assign to the current user
                        date_deadline=vehicle.acquisition_date + timedelta(days=60),
                        slug=carte_grise_activity_slug
                    )

                if (not visite_technique and (now.date() - vehicle.acquisition_date).days > 365 - days_before_visite_technique_alert) or (
                    visite_technique and (visite_technique.expiry_date - now.date()).days < days_before_visite_technique_alert
                ):
                    next_visite_technique_date = (
                        visite_technique.expiry_date if visite_technique else
                        vehicle.acquisition_date + timedelta(days=365)
                    )
                    vehicle.activity_schedule(
                        'mail.mail_activity_data_todo',
                        summary="Visite technique",
                        note=(
                            "La date de prochain visite technique pour cette véhicule est proche, "
                            f"veuillez penser de la ramener un garage avant le {next_visite_technique_date.strftime('%d/%m/%Y')}"
                        ),
                        user_id=self.env.user.id,
                        date_deadline=next_visite_technique_date,  # A year after registration
                        slug=auto_gen_slug
                    )

                if carte_grise:
                    if not vignette or ((vignette.expiry_date - now.date()).days < days_before_vignette_alert):
                        next_vignette_date = now.date() if not vignette else vignette.expiry_date
                        vehicle.activity_schedule(
                            'mail.mail_activity_data_todo',  # Activity type (default: To Do)
                            summary="Vignette introuvable.",  # Activity title
                            note="Vous devez ajouter la vignette pour cette véhicule.",  # Activity description
                            user_id=self.env.user.id,  # Assign to the current user
                            date_deadline=next_vignette_date,
                            slug=auto_gen_slug
                        )

                if not assurance or ((assurance.expiry_date - now.date()).days < days_before_assurance_alert):
                    next_assurance_date = now.date() if not assurance else assurance.expiry_date
                    vehicle.activity_schedule(
                        'mail.mail_activity_data_todo',  # Activity type (default: To Do)
                        summary="Assurance introuvable.",  # Activity title
                        note="Vous devez ajouter la assurance pour cette véhicule.",  # Activity description
                        user_id=self.env.user.id,  # Assign to the current user
                        date_deadline=next_assurance_date,
                        slug=auto_gen_slug
                    )

        return True

    @api.depends("acquisition_date")
    def _compute_has_alert(self):

        IrConfigParam = self.env['ir.config_parameter'].sudo()
        alert_message_km = int(IrConfigParam.get_param('vehicle_rental.alert_message_km', default=1000))
        w18_duration_default = int(IrConfigParam.get_param('vehicle_rental.w18_duration_default', default=1))
        recepisse_duration_default = int(IrConfigParam.get_param('vehicle_rental.recepisse_duration_default', default=2))
        carte_grise_duration_default = int(IrConfigParam.get_param('vehicle_rental.carte_grise_duration_default', default=10))

        danger_list = []
        warning_list = []
        self.has_alert_message = ""
        has_carte = True if len(self.paper_ids.filtered(lambda p: p.type_id.slug == "carte-grise")) > 0 else False
        has_recepisse = True if len(self.paper_ids.filtered(lambda p: p.type_id.slug == "recepisse")) > 0 else False
        has_W18 = True if len(self.paper_ids.filtered(lambda p: p.type_id.slug == "w18")) > 0 else False
        if self.acquisition_date and not has_carte:
            if not self._check_number_of_month_by_acquisition_date(w18_duration_default) and not has_W18 and not has_recepisse:
                danger_list.append("Ce véhicule a un document manquant <strong>(W18)</strong>.")
            elif self._check_number_of_month_by_acquisition_date(recepisse_duration_default) and not has_recepisse:
                danger_list.append("Ce véhicule a un document manquant <strong>(Carte Grise)</strong>.")
            elif self._check_number_of_month_by_acquisition_date(w18_duration_default) and not has_recepisse and not has_W18:
                danger_list.append("Ce véhicule a un document manquant <strong>(Récépissé)</strong>")
        # w18
        if not has_recepisse and not has_carte:
            msg = self._add_msg_to_alert(
                'w18',
                None,
                "Les jours restants pour la validité de <strong>W18</strong> du véhicule sont bientôt écoulés. Votre véhicule nécessite le Récépissé.",
                "<strong>W18</strong> du véhicule est expirée. Votre véhicule nécessite <strong>Récépissé</strong>.",
            )
            if msg != False:
                if msg[1] == 'danger':
                    danger_list.append(msg[0])
                else:
                    warning_list.append(msg[0])
        # Récépissé
        if not has_carte:
            msg = self._add_msg_to_alert(
                'recepisse',
                None,
                "Les jours restants pour la validité de <strong>Récépissé</strong> du véhicule sont bientôt écoulés. Votre véhicule nécessite La Carte Grise.",
                "<strong>Récépissé</strong> du véhicule est expirée. Votre véhicule nécessite La Carte Grise.",
            )
            if msg != False:
                if msg[1] == 'danger':
                    danger_list.append(msg[0])
                else:
                    warning_list.append(msg[0])
        # carte-grise
        msg = self._add_msg_to_alert(
            'carte-grise',
            None,
            "Les jours restants pour la validité de <strong>La Carte Grise</strong> du véhicule sont bientôt écoulés. Merci de la renouveler.",
            "<strong>La Carte Grise</strong> du véhicule est expirée. Merci de le renouveler.",
        )

        if msg != False:
            if msg[1] == 'danger':
                danger_list.append(msg[0])
            else:
                warning_list.append(msg[0])

        # Attestation d’Assurance
        msg = self._add_msg_to_alert(
            'attestation-dassurance',
            'Ce véhicule a un document manquant <strong>(Attestation d’assurance)</strong>.',
            "Les jours restants pour la validité de <strong>l'assurance</strong> du véhicule sont bientôt écoulés. Merci de la renouveler.",
            "<strong>L'assurance</strong> du véhicule est expirée. Merci de le renouveler.",
        )
        if msg != False:
            if msg[1] == 'danger':
                danger_list.append(msg[0])
            else:
                warning_list.append(msg[0])
        # Visite Technique
        msg = self._add_msg_to_alert(
            'visite-technique',
            'Ce véhicule a un document manquant <strong>(Visite technique)</strong>.',
            "Les jours restants pour la validité de <strong>la visite technique</strong> du véhicule sont bientôt écoulés. Merci de la renouveler.",
            "<strong>La visite technique</strong> du véhicule est expirée. Merci de la renouveler.",
        )
        if msg != False:
            if msg[1] == 'danger':
                danger_list.append(msg[0])
            else:
                warning_list.append(msg[0])
        # vignette
        msg = self._add_msg_to_alert(
            'vignette',
            'Ce véhicule a un document manquant <strong>(Vignette)</strong>.',
            "Les jours restants pour la validité de <strong>la vignette</strong> du véhicule sont bientôt écoulés. Vous devez la renouveler.",
            "<strong>La vignette</strong> du véhicule est expirée. Merci de la renouveler.",
        )
        if msg != False:
            if msg[1] == 'danger':
                danger_list.append(msg[0])
            else:
                warning_list.append(msg[0])

        # vidange
        last_vidange = self.env["fleet.vehicle.log.services"].search(
            domain=[
                ('vehicle_id', '=', self.id),
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
        if self.odometer - odometer_at_last_vidange  > vidange_lifespan_odometer:
            danger_list.append(f"Le véhicule a parcouru plus de {max_odometer_change_oil} km. Il est nécessaire de faire la vidange.")
        elif vidange_lifespan_odometer - (self.odometer - odometer_at_last_vidange) <= alert_message_km: # 9000
            warning_list.append("Ce véhicule aura bientôt besoin d'une <strong>vidange</strong>.")

        danger_list_html = "".join([f"<li>{item}</li>" for item in danger_list])
        warning_list_html = "".join([f"<li>{item}</li>" for item in warning_list])
        has_warning = len(warning_list) > 0
        has_danger = len(danger_list) > 0
        # if danger_list:
        html_content = f"""
            <div class="alert alert-danger {'d-none' if not has_danger else ''}" role="alert" >
                <ul>
                {danger_list_html}
                </ul>
            </div>
            <div class="alert alert-warning {'d-none' if not has_warning else ''}" role="alert" >
                <ul>
                {warning_list_html}
                </ul>
            </div>
        """
        self.has_alert_message = html_content

    def send_notification_change_oil(self):
        for vehicle in self:
            vehicle.activity_schedule(
                'mail.mail_activity_data_todo',  # Activity type (default: To Do)
                summary='Oil Change Reminder',
                note=f'The vehicle {vehicle.name} needs an oil change.',
                user_id=self.env.user.id  # Assign to the current user
            )
            return True



class FleetVehicleLogContract(models.Model):
    """Fleet Vehicle Log Contract"""
    _inherit = 'fleet.vehicle.log.contract'
    _description = __doc__

    license_plate = fields.Char(string="License Plate")
