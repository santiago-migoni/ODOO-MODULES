# Changelog

## Unreleased

### Added
- None.

### Changed
- None.

### Fixed
- None.

### Removed
- None.

## 19.0.1.0.0 - 2026-04-06

### Added
- V1 regression test suite with Python tests and HOOT coverage for the backend shell, home menu, WebClient, navbar, and list renderer scoping.
- Custom home menu shell for internal users as the backend landing experience.

### Changed
- Refactored navbar integration to preserve `web.NavBar` as the base component while extending the DIPLEG shell behavior.
- Established the DIPLEG backend design system across light and dark mode tokens, shell surfaces, and semantic state styling.
- Consolidated visual states for backend views and secondary components without changing layout structure.

### Fixed
- Restored compatibility with `website` and validated coexistence with `mail`, `portal`, `sale`, and `sale_management`.
- Hardened `WebClient`, `home_menu_service`, and `ListRenderer` behavior to keep the custom shell fail-safe and properly scoped.
- Stabilized HOOT and Python test cases for navbar behavior, logout cookie handling, and shell-related regressions.

### Removed
- None.
