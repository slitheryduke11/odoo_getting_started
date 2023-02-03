# -*- coding: utf-8 -*-

from odoo import Command, api, fields, models, _


class Property(models.Model):
	_inherit = 'estate.property'

	def action_sold_property(self):
		for record in self:
			self.env['account.move'].create(
				{
					'name': 'account',
					'partner_id': record.buyer_id.id,
					'move_type': 'out_invoice',
					'line_ids': [
						Command.create({
							'name': record.name,
							'quantity': 1.0,
							'price_unit': record.selling_price * 0.6
							})
					],
					'line_ids': [
						Command.create({
							'name': ' Administrative fees',
							'quantity': 1.0,
							'price_unit': 100.0
							})
					]
				}
			)

		return super().action_sold_property()