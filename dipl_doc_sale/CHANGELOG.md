# Changelog

## Unreleased

### Added
- Initial Odoo 19 scaffolding for `dipl_doc_sale` as a Dipleg-owned sales document module.
- New `Dipleg Commercial Quotation` PDF report action for `sale.order`.
- Report routing on `sale.order` so Argentine quotations and sales orders resolve to their dedicated document templates.
- Inherited `l10n_ar` header/footer integration for the sales document layout.

### Changed
- Established the `V1` policy that limits the module to the formal commercial quotation and defers internal/operational documents to later iterations.
- Refactored the quotation document to follow a near-mirror structural pattern of Argentine invoice and purchase documents, while keeping commercial and non-fiscal semantics.
- Reworked the report architecture so the main sales documents inherit `sale.report_saleorder_document` instead of rendering a fully standalone QWeb document.
