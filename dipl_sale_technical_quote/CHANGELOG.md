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
- Technical products now use `list_price` as the master price-per-kg source, while sales lines keep `dipl_price_per_kg` as the historical snapshot used by the technical calculation engine.
- Technical sales lines now rehydrate missing technical snapshot fields opportunistically on write and keep hidden snapshot fields in the inline sales list to prevent `Kilograms` from falling back to zero after reopening quotations.
- Technical sales lines now treat only thickness, density, and price-per-kg as the critical snapshot for calculation integrity, and backend writes protect those fields from degradant inline values before persisting.
- Technical sales lines now reset manual kilograms when product, quantity, flat pattern, or flat length changes, and normalize inline kilograms payloads consistently during create/write.

### Fixed
- Hardened `sale.order.line.write()` so partial inline saves can no longer zero-out a healthy technical snapshot and collapse `Kilograms` during save/reload flows.
- Prevented valid inline manual-kilogram payloads from being lost during line creation and blocked stale visible `Kilograms` values from reactivating manual override during technical edits.

### Removed
- None.
