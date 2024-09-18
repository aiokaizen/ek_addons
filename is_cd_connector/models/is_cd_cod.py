from odoo import models, fields, api, _
from odoo.exceptions import UserError
import base64
import xlrd
import os

class CODReport(models.Model):

    _name = "cod.report"

    name = fields.Char(string="Name", compute="_compute_name", store=True)  # Rapport_start_date_end_date
    file = fields.Binary(string="Rapport")
    cod_ids = fields.One2many('cod', inverse_name='report_id', string='Cod list')
    invoice_generated = fields.Boolean(default=False)
    file_name = fields.Char(string="File Name")  # Field to store the file name

    @api.depends('file_name')
    def _compute_name(self):
        for record in self:
            if record.file:
                # Extract file name without extension
                record.name = record.file_name
            else:
                record.name = "Rapport"

    @api.model
    def create(self, vals):
        """Overriding the create method and assigning
         the sequence for the record and other field validations."""
        records = super().create(vals)
        records.generate_cod()

        return records

    def action_generate_invoices(self):
        """Button action to generate invoices."""
        self.ensure_one()  # Ensure the method is called on a single record
        try:
            result = self.generate_invoices()  # Call the existing method to generate invoices
            return result
        except Exception as e:
            # Optional: Return an error notification if something goes wrong
            return {
                'type': 'ir.actions.client',
                'tag': 'display_notification',
                'params': {
                    'title': 'Error',
                    'message': 'An error occurred during the invoice generation: %s' % str(e),
                    'type': 'danger',  # For an error alert
                    'sticky': True,
                }
            }

    def generate_cod(self):

        # Ensure a file has been uploaded
        if not self.file:
            raise UserError("Please upload a valid Excel file.")

        # Decode the file and load it using xlrd
        try:
            file_content = base64.b64decode(self.file)
            workbook = xlrd.open_workbook(file_contents=file_content)
            sheet = workbook.sheet_by_index(0)  # Assuming data is in the first sheet
        except Exception as e:
            raise UserError("Invalid file format or content. Please upload a valid Excel file.")

        # Read and parse the Excel file row by row
        for rowx in range(1, sheet.nrows):  # Start from the second row, assuming the first is the header
            row = sheet.row(rowx)

            # Extract each cell's value from the row
            delivery_date = xlrd.xldate.xldate_as_datetime(row[0].value, workbook.datemode) if row[0].ctype == xlrd.XL_CELL_DATE else row[0].value
            tracking_id = row[1].value
            receive_state = row[4].value
            customer_name = row[5].value
            customer_contact = row[6].value
            customer_address = row[7].value
            customer_postcode = row[8].value
            granular_status = row[9].value
            shipper_name = row[10].value
            try:
                cod_amount = float(row[11].value)
            except:
                cod_amount = 0
            cod_fee = row[12].value
            status = 'Valid'
            if (not customer_name or not delivery_date or  
                not cod_amount or not customer_contact
            ): # should i have to add receive_state in this condition or not
                status = 'Invalid'
            
            if not tracking_id:
                continue


            # Create a new COD entry
            cod_entry = self.env['cod'].create({
                'report_id': self.id,
                'delivery_date': delivery_date or False,
                'tracking_id': tracking_id,
                'receive_state': receive_state,
                'customer_name': customer_name,
                'customer_contact': customer_contact,
                'customer_address': customer_address,
                'customer_postcode': customer_postcode,
                'granular_status': granular_status,
                'shipper_name': shipper_name,
                'cod_amount': cod_amount,
                'cod_fee': cod_fee,
                'status': status
            })

            # Search for or create the customer
            partner_id = self.env['res.partner'].search([('name', '=', customer_name), ('phone', '=', customer_contact)], limit=1)
            if not partner_id:
                partner_id = self.env['res.partner'].create({
                    'name': customer_name,
                    'phone': customer_contact,
                    'street': customer_address,
                    'zip': customer_postcode,
                })

        return {
                'type': 'ir.actions.client',
                'tag': 'display_notification',
                'params': {
                    'title': 'Success',
                    'message': 'The cods have been successfully generated!',
                    'type': 'success',  # For a success alert
                    'sticky': False,  # If True, the alert will stay until dismissed
                }
        }



    def generate_invoices(self):
        self.ensure_one()
        # Ensure a file has been uploaded
        if not self.file:
            raise UserError("Please upload a valid Excel file.")

        # Decode the file and load it using xlrd
        try:
            file_content = base64.b64decode(self.file)
            workbook = xlrd.open_workbook(file_contents=file_content)
            sheet = workbook.sheet_by_index(0)  # Assuming data is in the first sheet
        except Exception as e:
            raise UserError("Invalid file format or content. Please upload a valid Excel file.")

        # Read and parse the Excel file row by row
        product_id = 61  # Use your own product ID
        sequence_obj = self.env['ir.sequence']  
        cods = self.env['cod'].search([('report_id', '=', self.id)])
        for cod in cods:  # Start from the second row, assuming the first is the header
            if not cod.invoice_id:
                # Extract each cell's value from the row
                delivery_date = cod.delivery_date
                tracking_id = cod.tracking_id
                receive_state = cod.receive_state
                customer_name = cod.customer_name
                customer_contact = cod.customer_contact
                customer_address = cod.customer_address
                customer_postcode = cod.customer_postcode
                granular_status = cod.granular_status
                shipper_name = cod.shipper_name
                cod_amount = cod.cod_amount
                cod_fee = cod.cod_fee
                
                if cod.status == 'Invalid':
                    continue
                
                # Search for or create the customer
                partner_id = self.env['res.partner'].search([('name', '=', customer_name), ('phone', '=', customer_contact)], limit=1)
                if not partner_id:
                    partner_id = self.env['res.partner'].create({
                        'name': customer_name,
                        'phone': customer_contact,
                        'street': customer_address,
                        'zip': customer_postcode,
                    })
                # Create the draft invoice
                invoice = self.env['account.move'].create({
                    'move_type': 'out_invoice',
                    'partner_id': partner_id.id,
                    'invoice_date': delivery_date,
                    'invoice_line_ids': [(0, 0, {
                        'product_id': product_id,
                        'quantity': 1,  # Assume a quantity of 1, adjust as needed
                        'price_unit': cod_amount
                    })]
                })
                cod.write({
                    'invoice_id': invoice.id
                })
                self.write({
                    'invoice_generated': True
                })
        return {
            'type': 'ir.actions.client',
            'tag': 'display_notification',
            'params': {
                'title': 'Success',
                'message': 'The invoices have been successfully generated!',
                'type': 'success',
                'sticky': False,
            },
            'next': {
                'type': 'ir.actions.act_window',
                'res_model': 'cod',  # The model defined in the action
                'view_mode': 'tree',
                'domain': [('report_id', '=', self.id)],  # Set your dynamic domain
                # 'context': {'tree_view_edit': True},  # Additional context if needed
                'target': 'current',
                'name': 'Cod',
                'res_id': self.env.ref('is_cd_connector.action_cod_list_by_report_list').id  # Reference the action
            }
        }


class COD(models.Model):

    _name = "cod"
    _order = 'sequence asc'
    name = fields.Char(string='name')
    sequence = fields.Integer(string="Sequence", default=1)
    report_id = fields.Many2one("cod.report", "Rapport")
    delivery_date = fields.Date("Date of Delivery")
    tracking_id = fields.Char("Tracking ID")
    receive_state = fields.Char("Receiver State")
    customer_name = fields.Char("Customer Name")
    customer_contact = fields.Char("Customer Contact")
    customer_address = fields.Char("Customer Address")
    customer_postcode = fields.Char("Customer Postcode")
    granular_status = fields.Char("Granular Status")
    shipper_name = fields.Char("Shipper Name")
    cod_amount = fields.Float("COD Amount")
    cod_fee = fields.Char("COD Fee (Estimate)")
    status = fields.Selection([('Valid', 'Valid'), ('Invalid', 'Invalid')]) 
    invoice_id = fields.Many2one('account.move', string='Invoice')


    @api.model
    def create(self, vals):
        """Overriding the create method and assigning
         the sequence for the record and other field validations."""
        if vals.get('status') == 'Invalid':
            vals['sequence'] = 0
        if vals.get('name', _('New')) == _('New'):
            vals['name'] =  self.env['ir.sequence'].next_by_code(
                'cod') or _('New')
        return super().create(vals)