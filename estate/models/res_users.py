# -*- coding: utf-8 -*-

from odoo import fields, models


class Users(models.Model):
    _inherit = 'res.users'
    property_ids = fields.One2many(
        'estate.property', 'user_id',
        domain="['|', ('state', '=', 'new'), ('state', '=', 'offer_received')]")
