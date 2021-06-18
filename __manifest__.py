# Copyright 2020 Coop IT Easy SCRL fs
#   Vincent Van Rossem <vincent@coopiteasy.be>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
{
    "name": "Vracoop Custom Menu",
    "version": "12.0.1.0.0",
    "summary": """Menus""",
    "author": "Coop IT Easy SCRLfs, ",
    "website": "https://vracoop.fr/",
    "category": "Menu Items",
    "depends": [
        "account",
        "point_of_sale",
        "pos_container",
        "purchase",
        "sale",
        "stock",
    ],
    "data": [
        "views/account_menuitem.xml",
        "views/container.xml",
        "views/point_of_sale_view.xml",
        "views/pos_config_view.xml",
        "views/purchase_views.xml",
        "views/sale_views.xml",
        "views/stock_menu_views.xml",
    ],
    "installable": True,
}
