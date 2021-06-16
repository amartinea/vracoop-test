# Copyright 2019 Akretion (https://www.akretion.com).
# @author Pierrick Brun <pierrick.brun@akretion.com>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import fields, models


class ReportPosOrder(models.Model):
    _inherit = "report.pos.order"

    panier_moyen = fields.Float(
        string="Panier Moyen", readonly=True, group_operator="avg"
    )  # Le même champ que price_total mais groupé avec "AVG" et non "SUM"

    def _select(self):
        res = super(ReportPosOrder, self)._select()
        res += (
            ",AVG((l.qty * l.price_unit) * (100 - l.discount) / 100)"
            "AS panier_moyen"
        )
        return res
