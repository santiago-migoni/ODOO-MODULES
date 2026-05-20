# Changelog

## Unreleased

### Fixed
- Restored company CUIT rendering in the inherited `l10n_ar` header by falling back to `partner_id.vat` when the formatted AR VAT value is not available.
- Reverted the failed typography harmonization attempt and normalized the visible sales document wording to Spanish directly in QWeb.
- Aligned quotation and sales order headers, customer blocks, table labels, and footer behavior more closely with the AR invoice documentary family.
- Refactored the report source templates back to English and delegated Spanish rendering to `es_AR` translations, matching the benchmark policy used by `l10n_ar` and `l10n_ar_purchase`.
- Removed the generated `i18n` catalogs temporarily to validate the module with raw English source strings before regenerating translations from Odoo.
- Fixed the remaining quotation metadata label hardcoded in Spanish by switching `Validez` back to the English source string `Validity`.

### Changed
- Made header date labels translatable during the report wording refactor; translation catalogs are currently absent by design while raw English source validation is in progress.

### Added
- Initial Odoo 19 scaffolding for `dipl_doc_sale` as a Dipleg-owned sales document module.
- New `Dipleg Commercial Quotation` PDF report action for `sale.order`.
- Report routing on `sale.order` so Argentine quotations and sales orders resolve to their dedicated document templates.
- Inherited `l10n_ar` header/footer integration for the sales document layout.

### Historical Changes
- Established the `V1` policy that limits the module to the formal commercial quotation and defers internal/operational documents to later iterations.
- Refactored the quotation document to follow a near-mirror structural pattern of Argentine invoice and purchase documents, while keeping commercial and non-fiscal semantics.
- Reworked the report architecture so the main sales documents inherit `sale.report_saleorder_document` instead of rendering a fully standalone QWeb document.
