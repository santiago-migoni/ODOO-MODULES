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
- Technical products now keep only checkbox, thickness, density, and theoretical kilograms in their operational UI, while technical sales lines keep only `Flat Pattern`, `Flat Length`, `Kilograms`, and `Technical Price` as configurable visible columns.
- Technical sales lines now treat manual final prices as temporary overrides that are cleared by any technical change, while `Update Prices` remains the only explicit action that recomputes commercial pricing after a pricelist change.
- Technical sales lines now resolve kilograms through an explicit internal mode policy: `manual_kg` when both dimensions are empty and `geometry` when both are complete, while invalid mixed-dimension states are rejected.
- Manual kilogram entry now uses `dipl_kg_manual` as the only editable input in manual mode, while `dipl_kg_total` remains the derived effective value shown readonly for geometry lines.

### Fixed
- Hardened `sale.order.line.write()` so partial inline saves can no longer zero-out a healthy technical snapshot and collapse `Kilograms` during save/reload flows.
- Prevented valid inline manual-kilogram payloads from being lost during line creation and blocked stale visible `Kilograms` values from reactivating manual override during technical edits.
- Removed the ambiguous kilos override contract so `Kilograms` no longer flips unpredictably between computed and manual states during inline saves; geometry lines now ignore manual kg payloads and manual lines consume only `dipl_kg_manual`.
- Fixed the manual kilos UI flow so editing `Kilograms` in manual mode recalculates `Technical Price` and native `Unit Price` immediately instead of leaving the line at zero until save.

### Removed
- Legacy product metadata fields `dipl_material_code`, `dipl_thickness_label`, `dipl_requires_dimensions`, and `dipl_technical_notes` from the technical quotation model.
- Legacy sales-line metadata fields `dipl_material_code` and `dipl_thickness_label` from the technical snapshot.
