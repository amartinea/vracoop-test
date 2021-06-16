# Copyright 2019 Coop IT Easy SCRLfs
# @author Pierrick Brun <pierrick.brun@akretion.com>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import api, fields, models


class PosOrderLine(models.Model):
    _inherit = "pos.order.line"

    margin = fields.Float(string="Marge")
    margin_tx = fields.Float(string="Taux de Marge")

    def _compute_margins(self):
        for line in self.filtered("price_subtotal"):
            line.margin = line.price_subtotal - (
                line.product_id.standard_price * line.qty
            )
            line.margin_tx = (line.margin / line.price_subtotal) * 100


class PosOrder(models.Model):
    _inherit = "pos.order"

    margin_total = fields.Float(string="Marge")
    margin_tx = fields.Float(string="Taux de Marge")

    def action_pos_order_paid(self):
        res = super(PosOrder, self).action_pos_order_paid()
        for record in self:
            record.lines._compute_margins()
            record.margin_total = sum(record.lines.mapped("margin"))
            amount_ht = record.amount_total - record.amount_tax
            if amount_ht != 0:
                record.margin_tx = (record.margin_total / amount_ht) * 100
        return res


class PosSession(models.Model):
    _inherit = "pos.session"

    margin_total = fields.Float(string="Marge", compute="_compute_margins")
    margin_tx = fields.Float(
        string="Taux de Marge", compute="_compute_margins"
    )

    @api.depends("order_ids.margin_total")
    def _compute_margins(self):
        for record in self:
            orders = record.order_ids.filtered("margin_total")
            record.margin_total = sum(orders.mapped("margin_total"))
            total_amount_ht = sum(orders.mapped("amount_total")) - sum(
                orders.mapped("amount_tax")
            )
            if total_amount_ht != 0:
                record.margin_tx = record.margin_total / total_amount_ht * 100
