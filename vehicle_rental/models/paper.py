from datetime import datetime
from odoo import models, fields, api, _


class Paper(models.Model):
    """Paper Vehicule"""
    _name = "vehicle.rental.paper"
    _description = "Paper types"

    type_id = fields.Many2one("vehicle.rental.paper.type", string=_("Types"), required=True)
    issue_date = fields.Date(string=_("Date Début"), required=True)
    expiry_date = fields.Date(string=_("Date Fin"), required=True)
    owner_id = fields.Many2one("res.partner", string=_("Propriétaire"))
    vehicle_id = fields.Many2one("fleet.vehicle", required=True, string=_("Véhicule"))
    odometer = fields.Float(string=_("Odometer"), copy=False)
    


    @api.model
    def create(self, vals):
        # Example of custom logic for vidange
        print(vals["type_id"], " this is type paper after create ")
        vals["odometer"] = self.vehicle_id.odometer
        # Call the super method to create the record
        record = super(Paper, self).create(vals)
        
        return record