# Controller Pattern — Dipleg Odoo 19

Complete template for HTTP controllers. Use only when exposing endpoints for JSON APIs, web pages, or file downloads.

## Controller File (`controllers/{name}.py`)

```python
# -*- coding: utf-8 -*-
import logging

from odoo import http
from odoo.http import request

_logger = logging.getLogger(__name__)


class DiplExampleController(http.Controller):

    # === JSON endpoint (for JS/OWL calls) ===
    @http.route(
        "/dipl_example/data",
        type="json",
        auth="user",
        methods=["POST"],
    )
    def get_data(self, **kwargs):
        """Return data for the frontend."""
        records = request.env["dipl.example.model"].search_read(
            [("active", "=", True)],
            fields=["name", "state", "total"],
            limit=100,
        )
        return {"status": "ok", "data": records}

    # === HTTP endpoint (for web pages) ===
    @http.route(
        "/dipl_example/page",
        type="http",
        auth="public",
        website=True,
    )
    def example_page(self, **kwargs):
        """Render a public web page."""
        values = {
            "records": request.env["dipl.example.model"].sudo().search([]),
        }
        return request.render("dipl_example.page_template", values)

    # === Download endpoint ===
    @http.route(
        "/dipl_example/download/<int:record_id>",
        type="http",
        auth="user",
    )
    def download_report(self, record_id, **kwargs):
        """Stream a PDF report for download."""
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
```

## `controllers/__init__.py`

```python
from . import {name}
```

## Key conventions

| `auth=` | When to use |
|---|---|
| `"user"` | Requires a logged-in internal user. Default for backend endpoints. |
| `"public"` | Accessible without login (website pages, public APIs). |
| `"none"` | No session check at all — use only for webhooks with their own token validation. |

- **JSON endpoints** (`type="json"`): return a dict directly — Odoo serializes it. Do not call `json.dumps()`.
- **HTTP endpoints** (`type="http"`): return `request.render()` for templates or `request.make_response()` for files.
- **`sudo()` on public routes**: Always scope it — `sudo()` without a filter on a public endpoint is a security risk. Prefer `.sudo().search([("active", "=", True)])` with explicit domain.
- **Never use `auth="none"` without token validation** in the controller body.
- **Logging**: Use `_logger.warning(...)` for unexpected inputs, `_logger.info(...)` for significant events.
