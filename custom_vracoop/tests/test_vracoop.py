# Copyright 2019 Coop IT Easy (https://coopiteasy.be).
# @author Pierrick Brun <pierrick.brun@akretion.com>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo.tests.common import TransactionCase, Form, tagged


@tagged("post_install")
class TestVracoop(TransactionCase):
    def test_container_data_displayed(self):
        container = self.env.ref("pos_container.container_1")
        with Form(container) as container_form:
            self.assertEqual(container_form.name, "Container 1")
            self.assertEqual(container_form.barcode, "0498765456789")
            self.assertEqual(container_form.weight, 0.123)
