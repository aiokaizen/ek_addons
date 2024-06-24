from odoo import models, fields, _
from odoo.exceptions import ValidationError

class ReturnVehicleKmWizard(models.TransientModel):
    _name = 'return.vehicle.wizard'
    _description = 'Return Vehicle Wizard'

    kilometers = fields.Float(string='Kilometers')

    def confirm_return(self):
        contract = self.env['vehicle.contract'].browse(self.env.context.get('active_id'))
        
        if self.kilometers < contract.vehicle_id.odometer:
            raise ValidationError(_(f"Le relevé du compteur kilométrique doit être supérieur au dernier relevé du compteur ({contract.vehicle_id.odometer})Km."))

        if contract:
            contract.status = 'c_return'
            contract.vehicle_id.odometer = self.kilometers
            contract.return_odometer = self.kilometers
            odometer_data = {
                "vehicle_id": contract.vehicle_id.id,
                "value": self.kilometers,
                "date": fields.Date.today(),
            }
            self.env['fleet.vehicle.odometer'].create(odometer_data)
            
            return True
