# Changelog

## Unreleased

### Added
- Initial Odoo 19 module scaffolding for technical industrial quotations over Sales.
- Product-side technical quotation fields for material, thickness, density, and price per kg.
- Sales-line technical snapshot fields and minimal sales UI for technical quotation lines.
- Manual kg override with traceability for computed, manual, and effective kg on technical sales lines.
- Slice 03 technical pricing engine with native `sale.order.line` unit-price synchronization for technical lines.
- Slice 04 commercial integration for technical lines with native pricelist-aware pricing, manual final-price preservation, and pricing-state feedback in Sales.
- Technical product and sales-line UI simplification aligned with operator feedback: dedicated product tab, theoretical kilograms, and reduced technical columns in quotations.

### Changed
- Removed process from the initial technical product scaffold because it is not required in Slice 01.
- Technical sales lines now expose technical total and technical unit price in the sales UI and use the technical unit price as the native line `price_unit` bridge.
- Technical sales lines now treat `dipl_technical_price_unit` as the technical base, let compatible pricelist rules adjust the commercial price, ignore fixed-price pricelist rules, and preserve manual final price edits until native `Update Prices` is used.
- Technical sales lines now expose only `Flat Pattern`, `Flat Length`, `Kilograms`, and `Technical Price` as the main technical inputs in quotations, and products show only density, thickness, theoretical kilograms, and technical price in a dedicated tab.

### Fixed
- None.

### Removed
- None.
