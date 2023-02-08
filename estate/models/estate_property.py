# -*- coding: utf-8 -*-

from dateutil.relativedelta import relativedelta

from odoo import api, fields, models, _
from odoo.exceptions import UserError, ValidationError
from odoo.tools import float_utils


class Property(models.Model):
    _name = 'estate.property'
    _description = 'Real State Property'
    _order = 'id desc'

    name = fields.Char(required=True)
    description = fields.Text()
    postcode = fields.Char()
    date_availability = fields.Date(copy=False, default=lambda self: fields.Date.today() + relativedelta(months=3))
    expected_price = fields.Float(required=True)
    selling_price = fields.Float(readonly=True, copy=False)
    bedrooms = fields.Integer(default=2)
    living_area = fields.Integer()
    facades = fields.Integer()
    garage = fields.Boolean()
    garden = fields.Boolean()
    garden_area = fields.Integer()
    garden_orientation = fields.Selection([
        ('north', 'North'),
        ('south', 'South'),
        ('east', 'East'),
        ('west', 'West'),
    ])

    active = fields.Boolean(default=True)
    state = fields.Selection([
        ('new', 'New'),
        ('offer_received', 'Offer Received'),
        ('offer_accepted', 'Offer Accepted'),
        ('sold', 'Sold'),
        ('canceled', 'Canceled')
    ], required=True, copy=False, default='new')
    property_type_id = fields.Many2one('estate.property.type')
    buyer_id = fields.Many2one('res.partner', copy=False)
    salesperson_id = fields.Many2one('res.users', default=lambda self: self.env.user)
    tag_ids = fields.Many2many('estate.property.tag')
    offer_ids = fields.One2many('estate.property.offer', 'property_id')
    total_area = fields.Float(compute='_compute_total_area')
    best_price = fields.Float(compute='_compute_best_price')
    user_id = fields.Many2one('res.users')

    _sql_constraints = [
        ('check_expected_price', 'CHECK(expected_price > 0.0)',
         'The expected price must be strictly positive.'),
        ('check_selling_price', 'CHECK(selling_price > 0.0)',
         'The selling price must be positive.')
    ]

    @api.depends('living_area', 'garden_area')
    def _compute_total_area(self):
        for record in self:
            record.total_area = record.living_area + record.garden_area

    @api.depends('offer_ids')
    def _compute_best_price(self):
        for record in self:
            prices = record.mapped('offer_ids.price')
            record.best_price = max(prices) if len(prices) > 0 else 0.0

    @api.onchange('garden')
    def _onchange_garden(self):
        if self.garden:
            self.garden_area = 10
            self.garden_orientation = 'north'
        else:
            self.garden_area = 0
            self.garden_orientation = False

    def action_cancel_property(self):
        if self.state == 'sold':
            raise UserError(_('Sold properties cannot be canceled.'))
        self.state = 'canceled'
        return True

    def action_sold_property(self):
        if self.state == 'canceled':
            raise UserError(_('Canceled properties cannot be sold.'))
        self.state = 'sold'
        return True

    @api.constrains('selling_price', 'expected_price')
    def _check_selling_price(self):
        for record in self:
            if float_utils.float_is_zero(record.selling_price, precision_rounding=4):
                continue
            if float_utils.float_compare(record.selling_price, record.expected_price * 0.9, precision_digits=4) == -1:
                raise ValidationError(
                    _('The selling price must be at least 90% of the expected price! '
                        'You must reduce the expected price if you want to accept this offer.'))

    @api.ondelete(at_uninstall=False)
    def _check_state(self):
        for record in self:
            if record.state not in ['new', 'canceled']:
                raise ValidationError(_('Only properties with \'New\' or \'Cancelled\' status can be deleted.'))
