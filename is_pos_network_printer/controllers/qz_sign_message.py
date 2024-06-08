#
# Python Odoo example for controller.py
# Echoes the signed message and exits
#

#########################################################
#             WARNING   WARNING   WARNING               #
#########################################################
#                                                       #
# This file is intended for demonstration purposes      #
# only.                                                 #
#                                                       #
# It is the SOLE responsibility of YOU, the programmer  #
# to prevent against unauthorized access to any signing #
# functions.                                            #
#                                                       #
# Organizations that do not protect against un-         #
# authorized signing will be black-listed to prevent    #
# software piracy.                                      #
#                                                       #
# -QZ Industries, LLC                                   #
#                                                       #
#########################################################

import base64
from OpenSSL import crypto
from cryptography.hazmat.primitives.serialization import load_pem_private_key
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import padding, rsa

from odoo import http
from odoo.http import request



class SignMessage(http.Controller):

    @http.route('/qz-sign-message/', auth='public')
    def index(self, **kwargs):

        with open('ek_addons/is_pos_network_printer/security/private-key.pem', 'rb') as key_file:
            private_key = load_pem_private_key(key_file.read(), password=None)

        message = kwargs.get('request', '').encode()
        signature = private_key.sign(
            message,
            padding.PKCS1v15(),
            hashes.SHA1()
        )

        data_base64 = base64.b64encode(signature)
        return request.make_response(
            data_base64, [('Content-Type', 'text/plain')]
        )
