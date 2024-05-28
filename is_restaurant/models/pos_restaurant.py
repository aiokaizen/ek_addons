from odoo import fields, models, _


class RestaurantFloor(models.Model):

    _name = 'restaurant.floor'
    _inherit = 'restaurant.floor'

    # name = fields.Char('Floor Name', required=True)
    # pos_config_ids = fields.Many2many('pos.config', string='Point of Sales', domain="[('module_pos_restaurant', '=', True)]")


class RestaurantTable(models.Model):

    _name = 'restaurant.table'
    _inherit = 'restaurant.table'

    # name = fields.Char('Table Name', required=True, help='An internal identification of a table')
    # floor_id = fields.Many2one('restaurant.floor', string='Floor')
