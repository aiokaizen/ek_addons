from odoo import models, fields, api


class XMLIDMixin(models.AbstractModel):
    _name = "librarian.xmlid.mixin"
    _description = "Mixin to add XML ID field"

    xml_id = fields.Char(compute="_compute_xml_id", store=True, string="External ID")

    @api.depends("create_date", "write_date")
    def _compute_xml_id(self):
        for record in self:
            xml_id = self.env["ir.model.data"].search(
                [("model", "=", record._name), ("res_id", "=", record.id)], limit=1
            )
            record.xml_id = xml_id.complete_name if xml_id else ""
