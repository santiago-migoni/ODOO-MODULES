# Changelog

## Unreleased

## 19.0.1.3.2 - 2026-05-04

### Changed
- Rolled back home menu route strategy from canonical `/odoo/home` handling to action-based URL state (`action-dipl_web_theme.home_menu`) to restore previous navigation behavior.

## 19.0.1.3.1 - 2026-05-02

### Fixed
- Hardened login/home-menu frontend background asset so it no longer depends on backend-only SCSS tokens, avoiding frontend-minimal asset compilation failures.

## 19.0.1.3.0 - 2026-04-30

### Changed
- Replaced the home menu overlay URL cleanup strategy with a canonical router-based subapp route at `/odoo/home`.
- Updated shell navigation contracts so opening and closing the home menu transitions through stable route states instead of action URL rewrites.

### Fixed
- Eliminated route inconsistency between internal home-menu state and browser URL history during app-to-home and home-to-app transitions.

## 19.0.1.2.0 - 2026-04-30

### Changed
- Refactored home menu orchestration to run as webclient overlay state instead of client action navigation, keeping canonical `/odoo/` URL during shell usage.
- Hardened Community behavior by removing all remaining Studio-bridge runtime usage from the theme delivery.

### Fixed
- Prevented `/odoo/action-dipl_web_theme.home_menu` URL persistence when opening the home menu.

### Removed
- Optional `dipl_web_theme_studio_bridge` module and all associated "Add Custom Field" frontend integration paths.

## 19.0.1.1.0 - 2026-04-29

### Added
- Module documentation (`README.md`) with explicit Community/Enterprise compatibility policy and bridge strategy.

### Changed
- Hardened group configuration menu visibility so the "Automations" option only appears when automation opening is actually supported at runtime.
- Removed Studio-dependent list dropdown injection from the base theme module.

### Fixed
- Prevented backend JS crashes caused by Studio-specific handlers missing in standard list renderer contexts.

### Removed
- Base-theme coupling to `onSelectedAddCustomField` and related global list renderer override.

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
