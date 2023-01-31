# -*- coding: utf-8 -*-

from odoo import fields, models


class PropertyTag(models.Model):
    _name = 'estate.property.tag'
    _description = 'Real State Property Tag'

    name = fields.Char(required=True)

    _sql_constraints = [
        ('check_name', 'UNIQUE(name)',
         'The tag name must be unique.')
    ]
