# Copyright 2019 Coop IT Easy SCRLfs
# 	    Pierrick Brun <pierrick.brun@akretion.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import models, fields, api


class ProductTemplate(models.Model):
    _inherit = "product.template"

    margin = fields.Float(string="Marge", compute="_compute_margin")
    margin_tx = fields.Float(string="Taux de Marge", compute="_compute_margin")

    @api.depends("standard_price", "list_price", "taxes_id")
    def _compute_margin(self):
        for product in self:
            if product.standard_price:
                if len(product.taxes_id) == 1:
                    tax_amount = product.taxes_id.amount
                    prix_ht = product.list_price / (1 + (tax_amount / 100))
                    product.margin = prix_ht - product.standard_price
                    if prix_ht != 0:
                        product.margin_tx = (product.margin / prix_ht) * 100
                else:
                    product.margin = (
                        product.list_price - product.standard_price
                    )
                    if product.list_price != 0:
                        product.margin_tx = (
                            product.margin / product.list_price
                        ) * 100
