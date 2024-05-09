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

    @route('/api/chronodiali/test', auth='public', type="http")
    def test_handler(self):
        request.update_env(su=True)
        receiver = request.env['receiver'].create([{
            "api_url": "/api/chronodiali/test",
            "api_data": request.get_json_data(),
            "api_data2": json.dumps(request.get_json_data(), indent=4),
        }])
        return request.make_json_response({
            "status": "success",
            "data": receiver.read()
        })

    @route('/api/chronodiali/returned', auth='public', type="http")
    def returned_handler(self):
        request.update_env(su=True)
        receiver = request.env['receiver'].create([{
            "api_url": "/api/chronodiali/returned",
            "api_data": request.get_json_data(),
            "api_data2": json.dumps(request.get_json_data(), indent=4),
        }])
        return request.make_json_response({
            "status": "success",
            "data": receiver.read()
        })

    @route('/api/chronodiali/canceled', auth='public', type="http")
    def canceled_handler(self):
        request.update_env(su=True)
        receiver = request.env['receiver'].create([{
            "api_url": "/api/chronodiali/canceled",
            "api_data": request.get_json_data(),
            "api_data2": json.dumps(request.get_json_data(), indent=4),
        }])
        return request.make_json_response({
            "status": "success",
            "data": receiver.read()
        })

    @route('/api/chronodiali/delivery_success', auth='public', type="http")
    def delivery_success_handler(self):
        request.update_env(su=True)
        receiver = request.env['receiver'].create([{
            "api_url": "/api/chronodiali/delivery_success",
            "api_data": request.get_json_data(),
            "api_data2": json.dumps(request.get_json_data(), indent=4),
        }])
        return request.make_json_response({
            "status": "success",
            "data": receiver.read()
        })
