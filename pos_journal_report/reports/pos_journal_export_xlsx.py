# Copyright 2019 Coop IT Easy SCRLfs
# @author Pierrick Brun <pierrick.brun@akretion.com>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import models


class ZTicketExportXlsx(models.AbstractModel):
    _name = "report.pos_journal_report.journal_export_xlsx"
    _inherit = "report.report_xlsx.abstract"

    def _get_ws_params(self, wb, data, sessions):
        session_template = {
            "journal_code": {
                "header": {"value": "JournalCode"},
                "data": {
                    "value": self._render("session.config_id.journal_id.code")
                },
                "width": 20,
            },
            "journal_lib": {
                "header": {"value": "JournalLib"},
                "data": {
                    "value": self._render("session.config_id.journal_id.name")
                },
                "width": 20,
            },
            "ecriture_num": {
                "header": {"value": "EcritureNum"},
                "data": {"value": self._render("session.name")},
                "width": 20,
            },
            "ecriture_date": {
                "header": {"value": "EcritureDate"},
                "data": {
                    "value": self._render(
                        "'{:%Y%m%d}'.format(session.start_at)"
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
            "ecriture_num",
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
            "title": "sessions",
            "wanted_list": wanted_list,
            "col_specs": session_template,
        }
        ws_total_params = {
            "ws_name": "Totaux",
            "generate_ws_method": "_journal_report",
            "title": "totaux",
            "wanted_list": totaux_list,
            "col_specs": session_template,
        }

        return [ws_params, ws_total_params]

    def _aggregate_lines(self, lines, line, get_account):
        try:
            debit = line.amount
        except AttributeError:
            debit = 0
        try:
            credit = line.credit
        except AttributeError:
            credit = 0
        if credit == 0 and debit == 0 and hasattr(line, "debit"):
            # When there is a negative amount
            credit -= line.debit
        if not lines.get(get_account(line).id):
            lines[get_account(line).id] = {
                "acc": get_account(line),
                "debit": debit,
                "credit": credit,
            }
        else:
            lines[get_account(line).id]["debit"] += debit
            lines[get_account(line).id]["credit"] += credit

    def _journal_report(self, workbook, ws, ws_params, data, sessions):

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
        for session in sessions:
            lines = []
            obj_account_move_lines = self.env["account.move.line"].browse()
            stat_lines = {}
            for order in session.order_ids:
                for stat_line in order.statement_ids:
                    self._aggregate_lines(
                        stat_lines,
                        stat_line,
                        lambda x: x.statement_id.account_id,
                    )

                om = order.account_move
                # When order.account_move empty but the account.move exists
                if not om or len(om) == 0:
                    om = self.env["account.move"].search(
                        [
                            ("ref", "=", order.name),
                            ("journal_id", "=", order.sale_journal.id),
                        ],
                        limit=1,
                    )
                for om_line in om.line_ids:
                    # Ensure each line is unique
                    obj_account_move_lines |= om_line

            lines.extend(stat_lines.values())

            o_m_lines = {}
            for om_line in obj_account_move_lines:
                if om_line.account_id.user_type_id.type == "receivable":
                    # No account.move.lines for receivable account
                    # to avoid redundancy with statements
                    continue
                if not om_line.tax_ids and not om_line.tax_line_id:
                    account_missing_tva = self.env["account.account"].new(
                        {
                            "name": "TVA non renseignée (équivalent 0%)",
                            "code": self.env.ref(
                                "l10n_fr.1_tva_0"
                            ).account_id.code,
                        }
                    )
                    o_m_lines[0] = {
                        "acc": account_missing_tva,
                        "debit": 0,
                        "credit": 0,
                    }
                self._aggregate_lines(
                    o_m_lines, om_line, lambda x: x.account_id
                )

            lines.extend(o_m_lines.values())
            all_lines.extend(lines)

            if ws_params["title"] == "sessions":
                for line in lines:
                    row_pos = self._write_line(
                        ws,
                        row_pos,
                        ws_params,
                        col_specs_section="data",
                        render_space={"session": session, "line": line},
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
                lines_subtotal.values(),
                key=lambda x: x["credit"] - x["debit"]
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
