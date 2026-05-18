# Changelog

## Unreleased

### Fixed
- Rewired `stock.report_deliveryslip` to call the Dipleg stock document template so the standard `Delivery Slip` action renders the AR document structure at runtime.
- Replaced an invalid `t-field` on the stock address helper block with `t-out` so the delivery-slip template compiles correctly in QWeb runtime.
- Adopted the shared Dipleg header/footer path so stock documents stop duplicating the pager and use the common emitter block.
- Increased the spacing between the stock header, information block, and main logistics table to align with the common Dipleg print rhythm.

### Added
- Initial Odoo 19 implementation of the Dipleg AR stock document adapter over `stock`.

### Changed
- Refactored the module to own the standard stock delivery-slip flow instead of inheriting `l10n_ar_stock`.
- Added HTML render smoke coverage for outgoing, incoming, and internal stock documents.
- Replaced the standard stock address blocks with Dipleg AR partner and location sections so inventory documents follow the same formal structure as sales and purchases.
