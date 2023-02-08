# -*- coding: utf-8 -*-

from odoo import Command, models


class Property(models.Model):
    _inherit = 'estate.property'

    def action_sold_property(self):
        journal = self.env['account.journal'].search([('type', '=', 'sale')], limit=1)
        for record in self:
            self.env['account.move'].create(
                {
                    'name': 'account',
                    'partner_id': record.buyer_id.id,
                    'move_type': 'out_invoice',
                    'journal_id': journal.id,
                    'invoice_line_ids': [
                        Command.create({
                            'name': record.name,
                            'quantity': 1.0,
                            'price_unit': record.selling_price * 0.6
                        }),
                        Command.create({
                            'name': 'Administrative fees',
                            'quantity': 1.0,
                            'price_unit': 100.0
                        })
                    ]
                }
            )
        return super().action_sold_property()
