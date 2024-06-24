from odoo import http
from odoo.http import request
import json

class NotificationController(http.Controller):

    @http.route('/save-subscription/', type='json', auth='public', methods=['POST'], csrf=False)
    def save_subscription(self, **post):
        subscription = request.jsonrequest
        # Save the subscription to the database
        request.env['web.push.subscription'].sudo().create({
            'subscription_info': json.dumps(subscription)
        })
        return {'status': 'success'}
