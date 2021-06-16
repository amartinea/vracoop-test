# Copyright 2019 Coop IT Easy SCRLfs
# 	    Robin Keunen <robin@coopiteasy.be>
#           Pierrick Brun <pierrick.brun@akretion.com>
{
    "name": "Vacroop Custom",
    "version": "12.0.1.0.1",
    "summary": """
        Module spécifique à Vracoop""",
    "author": "Coop IT Easy SCRLfs, ",
    "website": "https://vracoop.fr/",
    "category": "Point of Sale",
    "depends": [
        "pos_container",
        "pos_ticket_logo",
        # 'pos_toledo_product',
        "pos_order_mgmt_container",
        "pos_discount",
        # 'l10n_fr_pos_cert', uniquement en France
    ],
    "data": [
        "data/barcode.xml",
        "templates/pos_templates.xml",
        "views/pos_config.xml",
        "views/pos_views.xml",
        "views/pos_products.xml",
        "views/report_pos_order.xml",
    ],
    "qweb": ["static/src/xml/pos.xml"],
    "installable": True,
}
