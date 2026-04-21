# Changelog

## Unreleased

## 19.0.1.1.0 - 2026-04-21

### Added
- Initial Odoo 19 module scaffolding for technical industrial quotations over Sales.
- Product-side technical quotation fields for technical products, including thickness, density, and theoretical kilograms.
- Sales-line technical snapshot fields and inline technical sales UI for quotation lines.
- Technical pricing engine with native `sale.order.line` unit-price synchronization for technical lines.
- Commercial integration for technical lines with native pricelist-aware pricing, explicit `Update Prices` behavior, and pricing-state feedback in Sales.

### Changed
- Technical products now use `list_price` as the master price-per-kg source, while sales lines keep `dipl_price_per_kg` as the historical snapshot used by the technical calculation engine.
- Technical sales lines now protect and rehydrate the critical snapshot (`thickness`, `density`, `price_per_kg`) during create/write so partial inline saves cannot collapse the technical calculation.
- Technical sales lines now clear manual final commercial price precedence whenever a technical input changes, while `Update Prices` remains the explicit recomputation path after pricelist changes.
- The module now follows a geometry-only policy: `Flat Pattern` and `Flat Length` are the only technical inputs in sales lines, while `Technical Kilograms` is always calculated and readonly.
- The operator-facing UI is reduced to the minimum technical set in product and sales views, keeping internal snapshot fields hidden from the normal sales flow.

### Fixed
- Save/reopen/edit flows no longer degrade a healthy technical snapshot to zero through partial inline payloads.
- Technical lines keep their geometry-based kilograms and pricing consistent after product changes, incomplete states, and explicit commercial recalculation.
- Incomplete technical lines remain storable with `Technical Kilograms`, `Technical Price`, and native `price_unit` at zero instead of raising invalid manual-kilogram behaviors.

### Removed
- Legacy product metadata fields `dipl_material_code`, `dipl_thickness_label`, `dipl_requires_dimensions`, and `dipl_technical_notes` from the technical quotation model.
- Legacy sales-line metadata fields `dipl_material_code` and `dipl_thickness_label` from the technical snapshot.
- Manual kilograms fields and related UI flow from the technical sales line model.
