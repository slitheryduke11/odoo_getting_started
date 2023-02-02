# -*- coding: utf-8 -*-

from dateutil.relativedelta import relativedelta

from odoo import api, fields, models, _
from odoo.exceptions import ValidationError


class PropertyOffer(models.Model):
    _name = 'estate.property.offer'
    _description = 'Real State Property Offer'
    _order = 'price desc'

    price = fields.Float()
    status = fields.Selection([
        ('accepted', 'Accepted'),
        ('refused', 'Refused'),
    ], copy=False)
    partner_id = fields.Many2one('res.partner', required=True)
    property_id = fields.Many2one('estate.property', required=True)
    validity = fields.Integer(default=7)
    date_deadline = fields.Date(compute='_compute_date_deadline', inverse='_inverse_date_deadline')
    property_type_id = fields.Many2one(related='property_id.property_type_id', store=True)

    _sql_constraints = [
        ('check_price', 'CHECK(price > 0.0)',
         'The offer price must be strictly positive.')
    ]

    @api.depends('create_date', 'validity')
    def _compute_date_deadline(self):
        for record in self:
            record.date_deadline = (record.create_date or fields.Date.today()) + relativedelta(days=record.validity)

    def _inverse_date_deadline(self):
        for record in self:
            record.validity = (record.date_deadline - record.create_date.date()).days

    def action_accept_offer(self):
        for record in self.property_id.offer_ids:
            if record.status == 'accepted':
                record.status = False
        self.status = 'accepted'
        self.property_id.buyer_id = self.partner_id
        self.property_id.selling_price = self.price
        self.property_id.state = 'offer_accepted' 
        return True

    def action_refuse_offer(self):
        if self.status == 'accepted':
            self.property_id.buyer_id = False
            self.property_id.selling_price = 0.0
        self.status = 'refused'
        return True

    @api.model
    def create(self, vals):
        offers = self.env['estate.property'].browse(vals['property_id']).offer_ids
        for offer in offers:
            if vals['price'] < offer.price:
                raise ValidationError(_('Can not create an offer with a lower amount than an existing offer.'))
        self.env['estate.property'].browse(vals['property_id']).state = 'offer_received'
        return super().create(vals)