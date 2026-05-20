# Changelog

## Unreleased

### Added
- Initial Odoo 19 scaffolding for `dipl_sale_internal_documents` as a Dipleg-owned internal sales document module.
- New `Cutting List` PDF report action for `sale.order`.
- New `Internal Sales Order` PDF report action for `sale.order`.
- Internal report templates that reuse the same documentary family as `dipl_doc_sale`.
- Technical line rendering based on `dipl_sale_technical_quote` fields on `sale.order.line`.

### Fixed
- Renamed the internal administrative document to `Internal Order` in both the report title and report action naming.
- Formatted `dipl_development_mm` and `dipl_width_mm` without decimals and `dipl_kg_total` with two decimals in the technical line tables.
- Simplified the `Cutting List` header and customer block so it only shows the customer name and suppresses company fiscal data plus customer address, VAT condition, CUIT, and salesperson.
