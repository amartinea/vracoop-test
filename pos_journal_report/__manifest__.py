# Copyright 2019 Coop IT Easy SCRLfs
#           Pierrick Brun <pierrick.brun@akretion.com>
{
    "name": "PoS Z Ticket",
    "version": "12.0.1.0.0",
    "summary": """Download a pos journal report as .xls""",
    "author": "Coop IT Easy SCRLfs, ",
    "website": "https://vracoop.fr/",
    "category": "Point of Sale",
    "depends": [
        "point_of_sale",
        "report_xlsx_helper",
        "l10n_fr",  # For O% TVA :/
    ],
    "data": ["views/pos_views.xml"],
    "installable": True,
}
