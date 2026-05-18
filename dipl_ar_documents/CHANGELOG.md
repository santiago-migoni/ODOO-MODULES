# Changelog

## Unreleased

### Added
- Initial Odoo 19 scaffolding for the shared Dipleg AR document framework addon.

### Changed
- Added a shared Dipleg emitter header template with explicit legal-name, address, VAT, CUIT, gross-income, and activity-start lines for all document adapters.
- Disabled the duplicated `external_layout_*` overrides so Dipleg reuses the single LATAM header/footer injection path and avoids double pagers in rendered PDFs.
- Hardened the base test suite to keep the core addon independent from `sale` and `purchase`.
- Added coverage for shared helper behavior used by the document adapters.
- Split the common document chrome into a header-only upper band plus a reusable body-level emitter block so vertical spacing no longer depends on PDF header reservation.

### Fixed
- Restored the company logo in the shared emitter header and widened the header-to-body spacing to match the requested document rhythm.
