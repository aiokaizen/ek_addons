from odoo import models, api, _
import xlsxwriter
import base64
from io import BytesIO
from odoo.exceptions import UserError

class SaleOrder(models.Model):
    _inherit = 'sale.order'

    def export_quotation_to_excel(self):
        self.ensure_one()
        # Create a new workbook
        output = BytesIO()
        workbook = xlsxwriter.Workbook(output)
        worksheet = workbook.add_worksheet('Quotations')

        # Set column widths for better readability
        worksheet.set_column('A:A', 20)
        worksheet.set_column('B:B', 30)
        worksheet.set_column('C:C', 20)
        worksheet.set_column('D:D', 20)
        worksheet.set_column('E:E', 15)
        worksheet.set_column('F:F', 15)
        worksheet.set_column('G:G', 15)
        worksheet.set_column('H:H', 10)
        worksheet.set_column('I:I', 10)

        # Company info formatting
        bold_format = workbook.add_format({'bold': True})
        normal_format = workbook.add_format()

        name = self.name or ''
        date_order = self.date_order.strftime('%d/%m/%Y') if self.date_order else ''
        partner_id = self.partner_id.name or ''
        # Write company information at the top
        worksheet.write('A1', 'Current Company Name', bold_format)
        worksheet.write('A2', 'Numero de devis:', normal_format)
        worksheet.write('B2', name, normal_format)
        worksheet.write('A3', 'Date de devis:', normal_format)
        worksheet.write('B3', date_order, normal_format)
        worksheet.write('A4', 'Client:', normal_format)
        worksheet.write('B4', partner_id, normal_format)

        # Write the header row starting from row 6
        headers = ['Référence/ISBN', 'Désignation/titre', 'Auteur', 'Éditeur', 'Catégorie', 'Sous-categorie', 'Année d\'édition', 'Quantité', 'Prix U', 'Remis %']
        header_format = workbook.add_format({'bold': True, 'border': 1})
        for col_num, header in enumerate(headers):
            worksheet.write(5, col_num, header, header_format)

        # Fill data starting from row 6
        row = 6


        # worksheet.write(row, 0, self.name or '', normal_format)
        # worksheet.write(row, 1, self.date_order.strftime('%d/%m/%Y') if self.date_order else '', normal_format)
        # worksheet.write(row, 2, self.partner_id.name or '', normal_format)
        # row += 1
        # for sale_order in self:
            # Write sale order specific info
            
            # Write order lines for each sale order
        for line in self.order_line:
            authors = line.product_id.author_ids if line.product_id and line.product_id.author_ids else []
            editor = line.product_id.editor_id.name if line.product_id and line.product_id.editor_id else ''
            worksheet.write(row, 0, line.product_id.default_code or '', normal_format)
            worksheet.write(row, 1, line.product_id.name or '', normal_format)
            worksheet.write(row, 2, ' '.join([author.name for author in authors]) or '', normal_format)  # Assuming you have author field
            worksheet.write(row, 3, editor or '', normal_format)  # Assuming you have publisher field
            worksheet.write(row, 4, line.product_id.categ_id.name or '', normal_format)  # Assuming category field
            worksheet.write(row, 5, line.product_id.categ_id.parent_id.name or '', normal_format)  # Assuming subcategory field
            worksheet.write(row, 6, line.product_id.release_year or '', normal_format)  # Assuming publication year field
            worksheet.write(row, 7, line.product_uom_qty or 0, normal_format)
            worksheet.write(row, 8, line.price_unit or 0, normal_format)
            worksheet.write(row, 9, line.discount or 0, normal_format)
            row += 1

        workbook.close()
        output.seek(0)
        xlsx_data = output.read()
        data_base64 = base64.b64encode(xlsx_data)

        attachment = self.env['ir.attachment'].create({
            'name': 'quotations.xlsx',
            'type': 'binary',
            'datas': data_base64,
            'mimetype': 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
        })

        return {
            'type': 'ir.actions.act_url',
            'url': f'/web/content/{attachment.id}?download=true',
            'target': 'new',
        }
