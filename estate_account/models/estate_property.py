# -*- coding: utf-8 -*-

from odoo import Command, api, fields, models, _

class Property(models.Model):
	_inherit = 'estate.property'

	# partner_id = self.buyer_id

	# partner_id = fields.Many2one('res.partner', copy=False)
	# property_type_id = fields.Many2one(related='property_id.property_type_id', store=True)
	# buyer_id =          fields.Many2one(related='res.partner', copy=False)


	# invoice_vendor_bill_id = fields.Many2one('account.move', store=False,
    #     check_company=True,
    #     string='Vendor Bill',
    #     help="Auto-complete from a past bill.")

	# move_id = fields.Many2one('account.move', string='Journal Entry',
    #     index=True, required=True, readonly=True, auto_join=True, ondelete="cascade",
    #     check_company=True,
    #     help="The move of this entry line.")




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