# Copyright 2019 Coop IT Easy SCRLfs
# @author Pierrick Brun <pierrick.brun@akretion.com>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import models


class InvoiceJournalExportXlsx(models.AbstractModel):
    _name = "report.invoice_journal_report.journal_export_xlsx"
    _inherit = "report.report_xlsx.abstract"

    def _get_ws_params(self, wb, data, invoices):
        invoice_template = {
            "journal_code": {
                "header": {"value": "JournalCode"},
                "data": {"value": self._render("invoice.journal_id.code")},
                "width": 20,
            },
            "journal_lib": {
                "header": {"value": "JournalLib"},
                "data": {"value": self._render("invoice.journal_id.name")},
                "width": 20,
            },
            "ecriture_date": {
                "header": {"value": "EcritureDate"},
                "data": {
                    "value": self._render(
                        "'{:%Y%m%d}'.format(invoice.date_invoice)"
                    )
                },
                "width": 20,
            },
            "compte_num": {
                "header": {"value": "CompteNum"},
                "data": {"value": self._render("line['acc'].code")},
                "width": 20,
            },
            "compte_lib": {
                "header": {"value": "CompteLib"},
                "data": {"value": self._render("line['acc'].name")},
                "width": 50,
            },
            "debit": {
                "header": {"value": "Debit"},
                "data": {"value": self._render("line['debit']")},
                "width": 20,
            },
            "credit": {
                "header": {"value": "Credit"},
                "data": {"value": self._render("line['credit']")},
                "width": 20,
            },
        }

        wanted_list = [
            "journal_code",
            "journal_lib",
            "ecriture_date",
            "compte_num",
            "compte_lib",
            "debit",
            "credit",
        ]
        totaux_list = [
            "compte_num",
            "compte_lib",
            "debit",
            "credit",
        ]
        ws_params = {
            "ws_name": "Sessions",
            "generate_ws_method": "_journal_report",
            "title": "invoices",
            "wanted_list": wanted_list,
            "col_specs": invoice_template,
        }
        ws_total_params = {
            "ws_name": "Totaux",
            "generate_ws_method": "_journal_report",
            "title": "totaux",
            "wanted_list": totaux_list,
            "col_specs": invoice_template,
        }

        return [ws_params, ws_total_params]

    def _aggregate_lines(self, lines, line):
        if not lines.get(line.account_id.id):
            lines[line.account_id.id] = {
                "acc": line.account_id,
                "debit": line.debit,
                "credit": line.credit,
            }
        else:
            lines[line.account_id.id]["debit"] += line.debit
            lines[line.account_id.id]["credit"] += line.credit

    def _journal_report(self, workbook, ws, ws_params, data, invoices):

        ws.set_portrait()
        ws.fit_to_pages(1, 0)
        ws.set_header(self.xls_headers["standard"])

        self._set_column_width(ws, ws_params)

        row_pos = 0
        row_pos = self._write_line(
            ws,
            row_pos,
            ws_params,
            col_specs_section="header",
            default_format=self.format_theader_yellow_left,
        )
        ws.freeze_panes(row_pos, 0)

        all_lines = []
        for invoice in invoices.filtered(lambda x: x.state == "paid"):
            lines = []
            payment_lines = {}
            for payment_line in invoice.payment_move_line_ids:
                for line in payment_line.move_id.line_ids.filtered(filter_4x_accounts):
                    # fetch reverse line from move
                    self._aggregate_lines(
                        payment_lines, line,
                    )
            lines.extend(payment_lines.values())

            i_m_lines = {}
            obj_account_move_lines = self.env["account.move.line"].browse()
            im = invoice.move_id
            # When invoice.account_move empty but the account.move exists
            if not im or len(im) == 0:
                im = self.env["account.move"].search(
                    [
                        ("ref", "=", invoice.reference),
                        ("journal_id", "=", invoice.journal_id.id),
                    ],
                    limit=1,
                )
            for im_line in im.line_ids:
                # Ensure each line is unique
                obj_account_move_lines |= im_line
            for im_line in obj_account_move_lines.filtered(filter_4x_accounts):
                if not im_line.tax_ids and not im_line.tax_line_id:
                    account_missing_tva = self.env["account.account"].new(
                        {
                            "name": "TVA non renseignée (équivalent 0%)",
                            "code": self.env.ref(
                                "l10n_fr.1_tva_0"
                            ).account_id.code,
                        }
                    )
                    i_m_lines[0] = {
                        "acc": account_missing_tva,
                        "debit": 0,
                        "credit": 0,
                    }
                self._aggregate_lines(
                    i_m_lines, im_line,
                )

            lines.extend(i_m_lines.values())
            all_lines.extend(lines)

            if ws_params["title"] == "invoices":
                for line in lines:
                    row_pos = self._write_line(
                        ws,
                        row_pos,
                        ws_params,
                        col_specs_section="data",
                        render_space={"invoice": invoice, "line": line},
                        default_format=self.format_tcell_left,
                    )
        if ws_params["title"] == "totaux":
            lines_subtotal = {}
            for line in all_lines:
                line_subtotal = lines_subtotal.get(line["acc"].code)
                if line_subtotal:
                    line_subtotal["debit"] += line["debit"]
                    line_subtotal["credit"] += line["credit"]
                else:
                    lines_subtotal[line["acc"].code] = line

            account_total = self.env["account.account"].new(
                {"name": "TOTAL", "code": ""}
            )
            total = {
                "acc": account_total,
                "debit": 0,
                "credit": 0,
            }
            for line_subtotal in sorted(
                lines_subtotal.values(), key=lambda x: x["credit"] - x["debit"]
            ):
                total["debit"] += line_subtotal["debit"]
                total["credit"] += line_subtotal["credit"]
                row_pos = self._write_line(
                    ws,
                    row_pos,
                    ws_params,
                    col_specs_section="data",
                    render_space={"line": line_subtotal},
                    default_format=self.format_tcell_left,
                )
            row_pos = self._write_line(
                ws,
                row_pos,
                ws_params,
                col_specs_section="data",
                render_space={"line": total},
                default_format=self.format_tcell_left,
            )

def filter_4x_accounts(line):
    # No account.move.lines for receivable or payable accounts
    # to avoid redundancy
    return line.account_id.user_type_id.type not in ["receivable", "payable"]
