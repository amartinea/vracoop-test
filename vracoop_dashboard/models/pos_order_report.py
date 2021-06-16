# Copyright 2019 Coop IT Easy SCRLfs
# @author Pierrick Brun <pierrick.brun@akretion.com>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import models, fields


class PosOrderReport(models.Model):
    _inherit = "report.pos.order"

    price_total_ht = fields.Float(string="Prix Total HT", readonly=True)
    margin_total = fields.Float(string="Marge", readonly=True)
    # margin_tx = fields.Float(string="Taux de Marge", readonly=True)

    def _select(self):
        res = super(PosOrderReport, self)._select()
        res += ", SUM(l.price_subtotal) AS price_total_ht"
        res += ", SUM(l.margin) AS margin_total"
        # res += ", SUM(l.margin) / SUM(l.price_subtotal) * 100 AS margin_tx"
        return res
