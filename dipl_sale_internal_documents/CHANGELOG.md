# Changelog

## Unreleased

### Added
- Initial Odoo 19 scaffolding for `dipl_sale_internal_documents` as a Dipleg-owned internal sales document module.
- New `Cutting List` PDF report action for `sale.order`.
- New `Internal Order` PDF report action for `sale.order`.
- Internal report templates that reuse the same documentary family as `dipl_doc_sale`.
- Technical line rendering based on `dipl_sale_technical_quote` fields on `sale.order.line`.

### Fixed
- Renamed the internal administrative document to `Internal Order` in both the report title and report action naming.
- Formatted `dipl_development_mm` and `dipl_width_mm` without decimals and `dipl_kg_total` with two decimals in the technical line tables.
- Simplified the `Cutting List` header and customer block so it only shows the customer name and suppresses company fiscal data plus customer address, VAT condition, CUIT, and salesperson.
- Restricted internal document printing to confirmed sales orders by removing generic report bindings, adding dedicated `sale.order` buttons, and validating the state in backend methods.
- Added `es_AR` translations for the new internal reports, buttons, action names, and backend validation message.
- Forced internal reports to render in the internal user language instead of the customer language.
- Explicitly cleared report bindings on both internal actions so upgrades remove stale Print-menu exposure from quotation state.
- Kept `binding_type` set to `report` while clearing `binding_model_id` so module upgrades do not fail on the required report-action field.
