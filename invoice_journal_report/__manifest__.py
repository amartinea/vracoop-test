# Copyright 2019 Coop IT Easy SCRLfs
#           Pierrick Brun <pierrick.brun@akretion.com>
{
    "name": "Invoice Journal report",
    "version": "12.0.1.0.0",
    "summary": """Download an invoice journal report as .xls""",
    "author": "Coop IT Easy SCRLfs, ",
    "website": "https://vracoop.fr/",
    "category": "Invoicing",
    "depends": [
        "account",
        "report_xlsx_helper",
        "l10n_fr",  # For O% TVA :/
    ],
    "data": ["views/invoice_views.xml"],
    "installable": True,
}
