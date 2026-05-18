# Changelog

## Unreleased

### Added
- Initial Odoo 19 scaffolding for the Dipleg AR purchase document adapter addon.

### Changed
- Implemented AR purchase report routing and the first Dipleg localized RFQ/purchase-order templates over the shared document core.
- Added HTML render smoke tests for RFQ and purchase-order report flows.
- Switched purchase documents to the shared Dipleg header so emitter information follows the common legal-name and per-field AR layout.

### Fixed
- Removed the obsolete purchase-order payment-terms XPath overrides that broke report compilation after the Dipleg information block replacement.
- Increased the spacing between the purchase header, information block, and main document table to align with the common Dipleg print rhythm.
- Tightened the purchase spacing scale to the shared `2 / 3 / 3` rhythm after validating the body-level emitter layout.

### Changed
- Adopted the body-level common emitter block so RFQ and purchase-order spacing no longer depends on PDF header geometry.
