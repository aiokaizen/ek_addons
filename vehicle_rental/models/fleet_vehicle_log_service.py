from odoo import api, fields, models, _

class FleetVehicleLogServiceProduct(models.Model):
    _name = 'fleet.vehicle.log.service.product'
    _description = 'Service Products for Vehicle Log Services'

    log_service_id = fields.Many2one('fleet.vehicle.log.services', string='Vehicle Log Service')
    product_id = fields.Many2one('product.product', string='Product')
    quantity = fields.Monetary(string='Quantity', default=1)
    price_unit = fields.Monetary(string='Unit Price')
    subtotal = fields.Monetary(string='Subtotal', compute='_compute_subtotal')

    amount_untaxed = fields.Monetary(string="Untaxed Amount", store=True, compute='_compute_amounts')
    amount_tax = fields.Monetary(string="Taxes", store=True, compute='_compute_amounts')
    amount_total = fields.Monetary(string="Total", store=True, compute='_compute_amounts')
    currency_id = fields.Many2one('res.currency', string='Currency', related='log_service_id.currency_id', store=True, readonly=True)

    @api.depends('quantity', 'price_unit')
    def _compute_subtotal(self):
        for record in self:
            record.subtotal = record.quantity * record.price_unit
    
    @api.onchange('product_id')
    def _onchange_product_id(self):

        if self.product_id:
            self.price_unit = self.product_id.lst_price

    @api.depends('subtotal')
    def _compute_amounts(self):
        for record in self:
            if record.product_id.taxes_id:
                tax_rate = record.product_id.taxes_id.amount / 100
                price_include = record.product_id.taxes_id.price_include
            else:
                tax_rate = 0
                price_include = True

            if not price_include:
                record.amount_untaxed = record.subtotal
                record.amount_total = record.amount_untaxed * (1 + tax_rate)
            else:
                record.amount_total = record.subtotal
                record.amount_untaxed = record.amount_total / (1 + tax_rate)

            record.amount_tax = record.amount_total - record.amount_untaxed
    
   
class FleetVehicleLogServices(models.Model):
    _inherit = 'fleet.vehicle.log.services'

    oil_change_odometer = fields.Integer(_("Vidange kilométrage"), default=10000)
    slug_service = fields.Char("slug", compute="_compute_slug_service",default=lambda self: self._default_slug())
    service_product_ids = fields.One2many('fleet.vehicle.log.service.product', 'log_service_id', string='Service Products')
    has_sale_order = fields.Boolean("Has sale order", compute="_compute_has_sale_order")
    
    amount_untaxed = fields.Monetary(string="Untaxed Amount", compute='_compute_total_amounts')
    amount_tax = fields.Monetary(string="Taxes", compute='_compute_total_amounts')
    amount_total = fields.Monetary(string="Total", compute='_compute_total_amounts')
    currency_id = fields.Many2one('res.currency', string='Currency', default=lambda self: self.env.company.currency_id.id)

    @api.onchange("service_type_id")
    def _onchange_slug_service(self):
        self.slug_service = self.service_type_id.slug

    @api.model
    def _default_slug(self):
        # Providing a default slug value based on service_type_id, if set
        if self.service_type_id:
            return self.service_type_id.slug
        return ''
    @api.depends("service_type_id")
    def _compute_slug_service(self):
        self.ensure_one()
        self.slug_service = self.service_type_id.slug

    def _get_sale_order(self):
        sale_order = self.env['sale.order'].search([
            ('vehicle_id', '=', self.vehicle_id.id),
            ('state', 'not in', ['cancel', 'draft'])
        ], limit=1)
        return sale_order
    @api.depends("vehicle_id")
    def _compute_has_sale_order(self):
        self.ensure_one()
        sale_order = self.env['sale.order'].search([
            ('vehicle_id', '=', self.vehicle_id.id),
            ('state', 'not in', ['cancel', 'draft'])
        ], limit=1)
        return len(sale_order) > 0

    def update_sale_order(self):
        sale_order = self._get_sale_order()
        if not sale_order:
            sale_order = self.env['sale.order'].create({
                'partner_id': self.vehicle_id.driver_id.partner_id.id,
                'vehicle_id': self.vehicle_id.id,
            })

        order_lines = []
        for product in self.service_product_ids:
            order_lines.append((0, 0, {
                'product_id': product.product_id.id,
                'product_uom_qty': product.quantity,
                'price_unit': product.price_unit,
            }))

        sale_order.write({
            'order_line': order_lines
        })
        return sale_order

    def action_create_sale_order(self):
        self.ensure_one()
        sale_order = self.env['sale.order'].create({
            'partner_id': self.vehicle_id.driver_id.id,
            'order_line': [(0, 0, {
                'product_id': line.product_id.id,
                'product_uom_qty': line.quantity,
                'price_unit': line.price_unit,
            }) for line in self.service_product_ids]
        })
        return {
            'type': 'ir.actions.act_window',
            'res_model': 'sale.order',
            'res_id': sale_order.id,
            'view_mode': 'form',
        }


    @api.depends('service_product_ids.amount_untaxed', 'service_product_ids.amount_tax', 'service_product_ids.amount_total')
    def _compute_total_amounts(self):
        for record in self:
            amount_untaxed = sum(product.amount_untaxed for product in record.service_product_ids)
            amount_tax = sum(product.amount_tax for product in record.service_product_ids)
            amount_total = sum(product.amount_total for product in record.service_product_ids)
            record.amount_untaxed = amount_untaxed
            record.amount_tax = amount_tax
            record.amount_total = amount_total


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    vehicle_id = fields.Many2one('fleet.vehicle.log.services', string=_("Vehicle"), required=True)