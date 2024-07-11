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


class VehicleImage(models.Model):
    """Vehicle Image"""
    _name = "vehicle.image"
    _description = __doc__

    avatar = fields.Binary(string="Avatar")
    vehicle_id = fields.Many2one('fleet.vehicle', ondelete="cascade")

class FleetVehicle(models.Model):
    """Fleet Vehicle"""
    _inherit = 'fleet.vehicle'
    _description = __doc__

    acquisition_date = fields.Date('Registration Date', required=True,
        default=fields.Date.today, help='Date of vehicle registration')

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

    is_old_vehicle = fields.Boolean(string='Is Old Vehicle', compute='_compute_is_old_vehicle')

    vehicle_image_ids = fields.One2many('vehicle.image', 'vehicle_id')
    # images = fields.Many2many('ir.attachment', string="Images")

    # video_file = fields.Binary(string="Video File")
    # video_filename = fields.Char(string="Video Filename")
    # video_url = fields.Char(string="Video URL", compute='_compute_video_url')

    # def _compute_video_url(self):
    #     for record in self:
    #         if record.video_file:
    #             record.video_url = '/web/content/vehicle_rental/%d/video_file/%s' % (record.id, record.video_filename)
    #         else:
    #             record.video_url = False

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
#             print("TEST", vehicle.name)

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


    @api.model
    def create_vehicle_papers_tasks(self):
        """
        This function creates the tasks related to the vehicle papers if they do not already exist.
        It is called from a cron job and other places.
        """
        now = fields.Datetime.now()
        vehicles = self.env["fleet.vehicle"].search([])

        for vehicle in vehicles:
            # IrConfigParam = self.env['ir.config_parameter'].sudo()
            auto_gen_slug = settings.VEHICLE_ACTIVITIES_AUTOMATIC_CREATION_SLUG
            # affected_user = self.env['res.users'].ref
            affected_user = self.env.ref("base.user_admin").id  # User to whome the task is affected.

            # Get data
            days_before_carte_grise_alert = self.env['vehicle.rental.paper.type'].search(
                [("slug", "=", "carte-grise")], limit=1
            ).days_to_alert
            carte_grise = vehicle.paper_ids.filtered(
                lambda p: p.type_id.slug == "carte-grise"
            )
            carte_grise = carte_grise[0] if carte_grise else None


            days_before_visite_technique_alert = self.env['vehicle.rental.paper.type'].search(
                [("slug", "=", "visite-technique")], limit=1
            ).days_to_alert
            visite_technique = vehicle.paper_ids.filtered(
                lambda p: p.type_id.slug == "visite-technique"
            )
            visite_technique = visite_technique[0] if visite_technique else None

            days_before_vignette_alert = self.env['vehicle.rental.paper.type'].search(
                [("slug", "=", "vignette")], limit=1
            ).days_to_alert
            vignette = vehicle.paper_ids.filtered(
                lambda p: p.type_id.slug == "vignette"
            )
            vignette = vignette[0] if vignette else None


            days_before_assurance_alert = self.env['vehicle.rental.paper.type'].search(
                [("slug", "=", "attestation-dassurance")], limit=1
            ).days_to_alert
            assurance = vehicle.paper_ids.filtered(
                lambda p: p.type_id.slug == "attestation-dassurance"
            )
            assurance = assurance[0] if assurance else None
            # Carte Grise
            carte_grise_activity_slug = f"{auto_gen_slug}_carte_grise_{carte_grise.id}" if carte_grise else (
                f"{auto_gen_slug}_carte_grise_{vehicle.id}_initial"
            )
            activity_carte_grise = self.env["mail.activity"].search(
                domain=[
                    ('slug', '=', carte_grise_activity_slug)
                ],
                limit=1
            )
            if not activity_carte_grise:
                if not carte_grise or ((carte_grise.expiry_date - now.date()).days < days_before_carte_grise_alert):
                    next_cart_grise_date = (
                        carte_grise.expiry_date if carte_grise else
                        vehicle.acquisition_date + timedelta(days=60)
                    )
                    vehicle.activity_schedule(
                        'mail.mail_activity_data_todo',  # Activity type (default: To Do)
                        summary="Carte grise introuvable.",  # Activity title
                        note="Vous devez ajouter une Carte Grise pour cette véhicule.",  # Activity description
                        user_id=affected_user,  # Assign to the current user
                        date_deadline=next_cart_grise_date,
                        slug=carte_grise_activity_slug
                    )

            # Visite Technique
            visite_technique_activity_slug = f"{auto_gen_slug}_visite_technique_{visite_technique.id}" if visite_technique else (
                f"{auto_gen_slug}_visite_technique_{vehicle.id}_initial"
            )
            activity_visite_technique_exist = len(self.env["mail.activity"].search(
                domain=[
                    ('slug', '=', visite_technique_activity_slug)
                ],
                limit=1
            )) > 0
            if not activity_visite_technique_exist:
                if (not visite_technique and (now.date() - vehicle.acquisition_date).days > 365 - days_before_visite_technique_alert) or (
                    visite_technique and (visite_technique.expiry_date - now.date()).days < days_before_visite_technique_alert
                ):
                    next_visite_technique_date = (
                        visite_technique.expiry_date if visite_technique else
                        vehicle.acquisition_date + timedelta(days=365)
                    )
                    vehicle.activity_schedule(
                        'mail.mail_activity_data_todo',
                        summary="Visite technique requise",
                        note=(
                            "La date de prochain visite technique pour cette véhicule est proche, "
                            f"veuillez penser de la ramener vers un garage avant le {next_visite_technique_date.strftime('%d/%m/%Y')}"
                        ),
                        user_id=affected_user,
                        date_deadline=next_visite_technique_date,  # A year after registration
                        slug=visite_technique_activity_slug
                    )

            # Vignette
            if carte_grise:
                vignette_activity_slug = f"{auto_gen_slug}_vignette_{vignette.id}" if vignette else (
                    f"{auto_gen_slug}_vignette_{vehicle.id}_initial"
                )
                activity_vignette_exist = len(self.env["mail.activity"].search(
                    domain=[
                        ('slug', '=', vignette_activity_slug)
                    ],
                    limit=1
                )) > 0
                if not activity_vignette_exist:
                    if not vignette or ((vignette.expiry_date - now.date()).days < days_before_vignette_alert):
                        next_vignette_date = now.date() if not vignette else vignette.expiry_date
                        vehicle.activity_schedule(
                            'mail.mail_activity_data_todo',  # Activity type (default: To Do)
                            summary="Vignette introuvable.",  # Activity title
                            note="Vous devez ajouter la vignette pour cette véhicule.",  # Activity description
                            user_id=affected_user,  # Assign to the current user
                            date_deadline=next_vignette_date,
                            slug=vignette_activity_slug
                        )

            # Assurance
            assurance_slug = f"{auto_gen_slug}_assurance_{assurance.id}" if assurance else (
                f"{auto_gen_slug}_assurance_{vehicle.id}_initial"
            )
            activity_assurance_exist = len(self.env["mail.activity"].search(
                domain=[
                    ('slug', '=', assurance_slug)
                ],
                limit=1
            )) > 0

            if not activity_assurance_exist:
                if not assurance or ((assurance.expiry_date - now.date()).days < days_before_assurance_alert):
                    next_assurance_date = now.date() if not assurance else assurance.expiry_date
                    vehicle.activity_schedule(
                        'mail.mail_activity_data_todo',  # Activity type (default: To Do)
                        summary="Assurance introuvable.",  # Activity title
                        note="Vous devez ajouter la assurance pour cette véhicule.",  # Activity description
                        user_id=affected_user,  # Assign to the current user
                        date_deadline=next_assurance_date,
                        slug=assurance_slug
                    )
            
            
            
            for paper in vehicle.paper_ids:

                if paper.type_id.slug in ('visite-technique', 'attestation-dassurance', 'vignette', 'w18', 'recepisse', 'carte-grise'):
                    continue
                
                paper_slug = f"{auto_gen_slug}_paper_{paper.id}" 
                activity_paper_exist = len(self.env["mail.activity"].search(
                    domain=[
                        ('slug', '=', paper_slug)
                    ],
                    limit=1
                )) > 0
                if activity_paper_exist:
                    continue
                if paper.expiry_date > now.date() or (paper.expiry_date - now.date()).days < paper.type_id.days_to_alert:
                    message = f"Vous devez ajouter le document {paper.type_id.name} pour cette véhicule."

                    vehicle.activity_schedule(
                        'mail.mail_activity_data_todo',  # Activity type (default: To Do)
                        summary=paper.type_id.name,  # Activity title
                        note=message,  # Activity description
                        user_id=affected_user,  # Assign to the current user
                        date_deadline=paper.expiry_date,
                        slug=paper_slug
                    )

                
        return True

    
    def send_notification_change_oil(self):
        for vehicle in self:
            vehicle.activity_schedule(
                'mail.mail_activity_data_todo',  # Activity type (default: To Do)
                summary='Oil Change Reminder',
                note=f'The vehicle {vehicle.name} needs an oil change.',
                user_id=self.env.user.id  # Assign to the current user
            )
            return True

    @api.depends('first_contract_date')
    def _compute_is_old_vehicle(self):
        today = fields.Datetime.now().date()

        for record in self:
            # we should use this field 'first_contract_date' instead of 'acquisition_date'
            if record.acquisition_date:
                record.is_old_vehicle = (today - record.acquisition_date).days > (3 * 365)
            else:
                record.is_old_vehicle = False


class FleetVehicleLogContract(models.Model):
    """Fleet Vehicle Log Contract"""
    _inherit = 'fleet.vehicle.log.contract'
    _description = __doc__

    license_plate = fields.Char(string="License Plate")
