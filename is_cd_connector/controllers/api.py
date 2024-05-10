import json
from odoo.http import (
    Controller, route, request
)


class CronoDialiAPI(Controller):

    @route([
        '/api/chronodiali/delivered',
        '/api/chronodiali/picked_up',
        '/api/chronodiali/test',
        '/api/chronodiali/returned',
        '/api/chronodiali/canceled',
        '/api/chronodiali/delivery_success',
    ], auth='public', type="http")

    def delivered_handler(self):
        request.update_env(su=True)
        receiver = request.env['receiver'].create([{
            "api_url": request.httprequest.full_path.split("?")[0],
            "api_data": request.get_json_data(),
            "api_data2": json.dumps(request.get_json_data(), indent=4),
            "api_get_params": json.dumps(request.get_http_params(), indent=4),
            "api_headers": json.dumps(dict(request.httprequest.headers), indent=4),
            "api_extra_info": json.dumps({
                "geoip": {
                    "country_code": request.geoip.country_code,
                    "country_name": request.geoip.country_name,
                    "ip": request.geoip.ip,
                },
                "context": request.context,
                "host": request.httprequest.host,
                "url": request.httprequest.url,
            }, indent=4),
        }])
        return request.make_json_response({
            "status": "success",
            "data": receiver.read()
        })
