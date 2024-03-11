import base64

from odoo import models, fields
from odoo.tools import file_open


class ResCompany(models.Model):

    _inherit = 'res.company'

    #----------------------------------------------------------
    # Default field values
    #----------------------------------------------------------

    def _get_logo(self):
        with file_open('muk_web_appsbar/static/src/img/logo_long_light.png', 'rb') as file:
            return base64.b64encode(file.read())

    #----------------------------------------------------------
    # Fields
    #----------------------------------------------------------

    appbar_image = fields.Binary(
        string='Apps Menu Footer Image',
        attachment=True, default=_get_logo
    )
