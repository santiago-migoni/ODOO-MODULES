# -*- coding: utf-8 -*-
"""Plantilla de controller HTTP estándar Dipleg.

Uso: copiar y adaptar para endpoints en módulos dipl_*.
Sigue Odoo 19 controller patterns.
"""
import json
import logging

from odoo import http
from odoo.http import request

_logger = logging.getLogger(__name__)


class DiplExampleController(http.Controller):

    # === JSON endpoint (para llamadas JS/OWL) ===#
    @http.route(
        "/dipl_example/data",
        type="json",
        auth="user",
        methods=["POST"],
    )
    def get_data(self, **kwargs):
        """Retorna datos para el frontend."""
        records = request.env["dipl.example.model"].search_read(
            [("active", "=", True)],
            fields=["name", "state", "total"],
            limit=100,
        )
        return {"status": "ok", "data": records}

    # === HTTP endpoint (para páginas web) ===#
    @http.route(
        "/dipl_example/page",
        type="http",
        auth="public",
        website=True,
    )
    def example_page(self, **kwargs):
        """Renderiza una página web."""
        values = {
            "records": request.env["dipl.example.model"].sudo().search([]),
        }
        return request.render("dipl_example.page_template", values)

    # === Download endpoint ===#
    @http.route(
        "/dipl_example/download/<int:record_id>",
        type="http",
        auth="user",
    )
    def download_report(self, record_id, **kwargs):
        """Descarga un reporte PDF."""
        record = request.env["dipl.example.model"].browse(record_id)
        if not record.exists():
            return request.not_found()

        pdf_content, _ = request.env["ir.actions.report"]._render_qweb_pdf(
            "dipl_example.report_template", [record.id]
        )
        return request.make_response(
            pdf_content,
            headers=[
                ("Content-Type", "application/pdf"),
                (
                    "Content-Disposition",
                    f'attachment; filename="report_{record.name}.pdf"',
                ),
            ],
        )
