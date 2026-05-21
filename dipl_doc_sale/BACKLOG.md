# Backlog

## Immediate

### 1. Reconcile sales document structure with AR invoice base
- Priority: High
- Problem: `dipl_doc_sale` already reuses the `l10n_ar` documentary header, but the body still inherits `sale.report_saleorder_document`, which differs structurally from the AR invoice family in `account.report_invoice_document`.
- Evidence:
  - `l10n_ar.custom_header` provides the documentary top block.
  - `account.report_invoice_document` provides the invoice-family information block and line table grammar.
  - `sale.report_saleorder_document` still drives the current sales body layout.
- Impact:
  - document titles, label casing, spacing, table density, and totals still drift from the AR invoice benchmark.
- Files involved:
  - `dipl_doc_sale/report/quote_report_templates.xml`
- Closure criteria:
  - quotation and sales order visually read as part of the same family as the AR invoice, not just as sales reports with an AR header.

### 2. Rebuild the information block against the invoice-family grammar
- Priority: High
- Problem: the current `#informations` block is sales-specific and not aligned with the exact composition used by `l10n_ar` on invoices.
- Target:
  - left column with partner identification
  - right column with commercial metadata
  - label/value rhythm matching the invoice document
- Files involved:
  - `dipl_doc_sale/report/quote_report_templates.xml`
- Closure criteria:
  - labels, spacing, and grouping match the AR invoice documentary style more closely.

### 3. Rework the line table and totals to invoice-like structure
- Priority: High
- Problem: even after fixing broken `xpath` anchors, the sales table is still based on `sale.report_saleorder_document`, not on the invoice-family table contract.
- Impact:
  - the table still differs in weight, spacing, and documentary density from the AR invoice.
- Files involved:
  - `dipl_doc_sale/report/quote_report_templates.xml`
- Closure criteria:
  - line table, taxes column, and totals block align visually with the invoice benchmark.

## Architecture

### 4. Introduce a shared Dipleg document layout module
- Priority: Medium
- Problem: `dipl_doc_sale` is carrying both business semantics and cross-document visual rules. That increases duplication risk if Dipleg later wants the same documentary family for sales, purchases, and accounting documents.
- Proposal:
  - create a shared layout module such as `dipl_doc_layout` or `dipl_doc_document`
  - centralize:
    - documentary header
    - documentary footer
    - reusable information blocks
    - reusable table/totals visual contracts
  - keep business-specific semantics in downstream modules such as:
    - `dipl_doc_sale`
    - future `dipl_doc_purchase`
    - future `dipl_doc_account`
- Expected benefit:
  - one visual source of truth for Dipleg documents
  - lower drift between quotation, sales order, purchase, and invoice-style outputs
  - smaller functional modules with clearer ownership
- Constraints:
  - do not mix fiscal logic into the layout base
  - first define a narrow shared contract before extracting code
- Closure criteria:
  - a concrete design exists for a shared documentary layout layer and `dipl_doc_sale` can delegate common visual structure to it instead of owning everything locally.
