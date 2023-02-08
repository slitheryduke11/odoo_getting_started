# -*- coding: utf-8 -*-

from odoo import api, fields, models


class PropertyType(models.Model):
    _name = 'estate.property.type'
    _description = 'Real State Property Type'
    _order = 'sequence, name'

    name = fields.Char(required=True)
    property_ids = fields.One2many('estate.property', 'property_type_id')
    sequence = fields.Integer(default=1, help='Used to order types.')
    offer_ids = fields.One2many('estate.property.offer', 'property_type_id')
    offer_count = fields.Integer(compute='_compute_offer_count')

    _sql_constraints = [
        ('check_name', 'UNIQUE(name)',
         'The property type must be unique.')
    ]

    @api.depends('offer_ids')
    def _compute_offer_count(self):
        for record in self:
            record.offer_count = len(record.mapped('offer_ids.price'))
