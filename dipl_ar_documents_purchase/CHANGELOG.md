# Changelog

## Unreleased

### Added
- Initial Odoo 19 scaffolding for the Dipleg AR purchase document adapter addon.

### Changed
- Implemented AR purchase report routing and the first Dipleg localized RFQ/purchase-order templates over the shared document core.
- Added HTML render smoke tests for RFQ and purchase-order report flows.
- Switched purchase documents to the shared Dipleg header so emitter information follows the common legal-name and per-field AR layout.
- Fixed a purchase-order QWeb regression where the payment-terms override could replace the whole page and generate a blank PDF.
