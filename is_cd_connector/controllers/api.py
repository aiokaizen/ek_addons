import json
from odoo.http import (
    Controller, route, request
)


class CronoDialiAPI(Controller):

    @route('/api/chronodiali/delivered', auth='public', type="http")
    def delivered_handler(self):
        request.update_env(su=True)
        receiver = request.env['receiver'].create([{
            "api_url": "/api/chronodiali/delivered",
            "api_data": request.get_json_data(),
            "api_data2": json.dumps(request.get_json_data(), indent=4),
        }])
        return request.make_json_response({
            "status": "success",
            "data": receiver.read()
        })

    @route('/api/chronodiali/picked_up', auth='public', type="http")
    def picked_up_handler(self):
        request.update_env(su=True)
        receiver = request.env['receiver'].create([{
            "api_url": "/api/chronodiali/picked_up",
            "api_data": request.get_json_data(),
            "api_data2": json.dumps(request.get_json_data(), indent=4),
        }])
        return request.make_json_response({
            "status": "success",
            "data": receiver.read()
        })
