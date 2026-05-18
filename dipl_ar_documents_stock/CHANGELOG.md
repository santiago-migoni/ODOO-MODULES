# Changelog

## Unreleased

### Added
- Initial Odoo 19 implementation of the Dipleg AR stock document adapter over `stock`.

### Changed
- Refactored the module to own the standard stock delivery-slip flow instead of inheriting `l10n_ar_stock`.
- Added HTML render smoke coverage for outgoing, incoming, and return stock documents.
