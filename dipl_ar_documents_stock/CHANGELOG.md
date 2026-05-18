# Changelog

## Unreleased

### Added
- Initial Odoo 19 implementation of the Dipleg AR stock document adapter over `stock`.

### Changed
- Refactored the module to own the standard stock delivery-slip flow instead of inheriting `l10n_ar_stock`.
- Added HTML render smoke coverage for outgoing, incoming, and internal stock documents.
- Replaced the standard stock address blocks with Dipleg AR partner and location sections so inventory documents follow the same formal structure as sales and purchases.
