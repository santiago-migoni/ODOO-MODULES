# Changelog

## Unreleased

### Added
- Initial Odoo 19 scaffolding for the Dipleg AR sale document adapter addon.

### Changed
- Implemented AR sale report routing and the first Dipleg localized quotation/order template over the shared document core.
- Added HTML render smoke tests for quotation, sales order, and pro-forma report flows.
- Switched sales documents to the shared Dipleg header so emitter information follows the common legal-name and per-field AR layout.

### Fixed
- Increased the spacing between the sale header, information block, and main document table to align with the common Dipleg print rhythm.
