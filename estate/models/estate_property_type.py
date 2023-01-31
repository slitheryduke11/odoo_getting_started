# -*- coding: utf-8 -*-

from odoo import fields, models


class PropertyType(models.Model):
    _name = 'estate.property.type'
    _description = 'Real State Property Type'

    name = fields.Char(required=True)

    _sql_constraints = [
        ('check_name', 'UNIQUE(name)',
         'The property type must be unique.')
    ]