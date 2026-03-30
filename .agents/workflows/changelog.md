---
description: Genera o actualiza CHANGELOG.md con versionado semántico en un módulo de Odoo 19.
---
# Changelog Workflow (Fase 6 — Deploy)

Generate or update the `CHANGELOG.md` of a Dipleg custom module before any deploy.

The argument `$ARGUMENTS` contains the module name and the new version number (e.g., `dipl_sale_extra 19.0.1.2.0`).

---

## When to run

Run this workflow **before every deploy**, as the last step before `/deploy`:
1. After all Quality Gates pass (Fase 5 completed).
2. After `version` in `__manifest__.py` has been bumped.
3. Before creating the Pull Request.

---

## Step 1 — Determine the change type

Read the git diff or ask the user what was done:

| Change type | CHANGELOG section | Version increment |
|---|---|---|
| New model, new feature, new report | `Added` | Minor `Y` |
| Behavior change, UI update | `Changed` | Minor `Y` |
| Bug fix (no schema change) | `Fixed` | Patch `Z` |
| Model rename, field removal, API breaking | `Changed` + migration note | Major `X` |
| Feature/field removed intentionally | `Removed` | Minor `Y` or Major `X` |
| Known issue without fix yet | `Deprecated` | No version change |

## Step 2 — Locate or create CHANGELOG.md

The file must be at the module root: `dipl_{name}/CHANGELOG.md`.

If it does not exist, create it with this header:

```markdown
# Changelog — Dipleg {Module Display Name}

All notable changes to this module are documented here.
Format follows [Keep a Changelog](https://keepachangelog.com/en/1.0.0/).
Versioning follows `19.0.X.Y.Z` semantic versioning.

---
```

## Step 3 — Add the new entry

Prepend the new version block **at the top** (below the header), before existing entries:

```markdown
## [19.0.X.Y.Z] - YYYY-MM-DD

### Added
- Brief description of new feature or field. (Ref: STORY-XXX if applicable)

### Changed
- What behavior changed and why it was necessary.

### Fixed
- Root cause of the bug. Fix: what was changed to resolve it.

### Removed
- What was removed and why.
```

Rules:
- Only include sections that apply — omit empty sections (`Added`, `Changed`, etc.).
- One bullet per change — keep each line under 120 characters.
- Write in English (code and docs are English; UI strings are translated separately).
- Reference story IDs (`STORY-XXX`) when available.

## Step 4 — Verify consistency

Before committing:
- [ ] `version` in `__manifest__.py` matches the new CHANGELOG entry version.
- [ ] The date is today's date in `YYYY-MM-DD` format.
- [ ] No section is left with placeholder text.
- [ ] The entry accurately reflects the diff (no over-summarizing or omissions).

## Example: complete CHANGELOG.md

```markdown
# Changelog — Dipleg Sale Extra

All notable changes to this module are documented here.
Format follows [Keep a Changelog](https://keepachangelog.com/en/1.0.0/).
Versioning follows `19.0.X.Y.Z` semantic versioning.

---

## [19.0.1.2.1] - 2025-11-15

### Fixed
- Computed field `total_approved` returned incorrect value when lines had
  zero quantity. Fix: added zero-guard in `_compute_total_approved`.

## [19.0.1.2.0] - 2025-10-30

### Added
- New field `approved_by` (Many2one to `res.users`) on `dipl.sale.extra`.
- Action button `action_approve` with state transition `draft` → `approved`.

### Fixed
- Missing Spanish translation for "Approve" button label.

## [19.0.1.1.0] - 2025-09-01

### Added
- Initial module release with `dipl.sale.extra` model.
```
