from odoo import fields, models, api, _
from odoo.exceptions import UserError


class InsightSphereConfig(models.Model):

    _name = 'config'
    _description = "Insight Sphere base configuration"

    name = fields.Char(required=True)
    activate_invoincing_policy = fields.Boolean(
        "Activate invoicing policy", default=False
    )

    @classmethod
    def get_instance(cls):
        if not hasattr(cls, 'instance'):
            cls.instance = cls._create_default_instance()
        return cls.instance
    
    @classmethod
    def _create_default_instance(cls):
        return cls.create({
            "name": "Insight Sphere Settings",
        })

    @api.model
    def create(self, vals_list):
        first_record = self.env['config'].search([], limit=1)
        print("First record:", first_record)
        if first_record.exists():
            print("Return existing record")
            return first_record

        print("Creating first record")
        return super().create(vals_list)

    def unlink(self):
        if self.env['config'].search_count([]) == 1:
            raise UserError("Cannot delete the singleton instance of Insight Sphere configuration.")
        else:
            return super(InsightSphereConfig, self).unlink()