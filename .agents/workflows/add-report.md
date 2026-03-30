---
description: Crea un reporte QWeb (PDF/HTML) en un módulo de Odoo 19.
---
# Add Report Workflow

Step-by-step process to generate a new QWeb report for an Odoo 19 model.

The argument `$ARGUMENTS` contains the report name and module.

## 1. Context

1. Define the report type:
    - **PDF**: printed document with Odoo header/footer (`qweb-pdf`).
    - **HTML**: on-screen view (`qweb-html`).
2. Identify the target model for data rendering.
3. Determine: data fields, grouping needs, and paper format (A4 Portrait / Landscape).

## 2. Technical proposal

Present:
- `report/{report_name}_templates.xml` (QWeb template).
- `report/{report_name}_reports.xml` (`ir.actions.report` action).
- Custom paper format (if size/margins differ from Odoo default).

**WAIT FOR USER APPROVAL.**

## 3. Implementation

1. **Register action** (`ir.actions.report`): `report_type = "qweb-pdf"` or `"qweb-html"`.
2. **Template root call**:
    - PDF: `t-call="web.external_layout"` — includes Odoo's corporate header/footer.
    - HTML: `t-call="web.html_container"` — plain container for on-screen display.
3. **Data rendering**: Use `t-out` (never `t-raw`) for all dynamic content.
4. **Manifest**: Add both XML files to `data:` in the correct load order (action after template).

## 4. Edge cases

- **Grouped data / subtotals**: Use `t-foreach` on pre-grouped data from the model's `_read_group()`. Avoid computing aggregates in QWeb.
- **Multi-language**: Use `t-lang="o.partner_id.lang"` on the root element to render in the partner's language.
- **Custom paper format**: Define `report.paperformat` record and reference it in the action.

## 5. Verification

1. Print a test PDF from the record's "Print" action menu.
2. Confirm header/footer appear correctly (only on PDF).
3. Check Odoo server logs for rendering errors.
