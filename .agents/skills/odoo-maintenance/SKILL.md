---
name: odoo-maintenance
description: >-
  Post-deploy maintenance specialist for Odoo 19 custom modules. Use at Fase 7
  (Mantenimiento) for production bug fixes, hotfix decisions, semantic
  versioning, and post-deploy monitoring. Activate with keywords: production
  bug, hotfix, version bump, maintenance, post-deploy, module version.
---

# Odoo Maintenance Skill

**Role:** Fase 7 — Maintenance specialist for Dipleg's Odoo 19 modules in production

**Activate when:** A module is in production and requires a bug fix, improvement, version update, or post-deploy monitoring.

## Lean Principle

> Muda of repair: the cost of fixing a production bug is 10–100x the cost of catching it in QA.
> Every maintenance action is evidence of a gap in a previous phase — document it to prevent recurrence.

---

## Decision Tree: What type of maintenance?

```
Production issue reported
        │
        ▼
Is it breaking core functionality for users right now?
        │
       YES → /hotfix protocol (accelerated, same-day)
        │
        NO
        │
        ▼
Is it a bug (incorrect behavior)?
        │
       YES → /fix-issue → normal release cycle
        │
        NO
        │
        ▼
Is it a feature request or improvement?
        │
       YES → Re-enter SDLC from Fase 1 (Planificación)
        │
        NO
        │
        ▼
Is it a performance or security observation?
        │
       YES → /perf-check or /security-audit → improvement sprint
```

---

## Semantic Versioning Protocol

All `dipl_*` modules use `19.0.X.Y.Z`:

| Increment | When | Action required |
|---|---|---|
| **Major `X`** | Breaking change: model renamed, field deleted, API incompatible | Migration script in `migrations/19.0.X.0.0/` mandatory |
| **Minor `Y`** | New feature, backward-compatible | No migration; new fields with defaults are safe |
| **Patch `Z`** | Bug fix, no schema change | No migration needed |

**Rule:** Always update `version` in `__manifest__.py` AND add entry to `CHANGELOG.md` before any deploy.

```python
# Example version bump in __manifest__.py
"version": "19.0.1.2.1",  # was 19.0.1.2.0 — patch for bug fix
```

---

## Post-Deploy Monitoring Protocol

### Immediately after deploy (first 30 minutes)
- Monitor Odoo.sh build logs until 🟢
- Check server logs for tracebacks: `tail -f /var/log/odoo/odoo-server.log`
- Run the core user flow manually with production data

### First 24 hours
- Check server logs for recurring warnings or errors
- Verify computed fields are displaying correctly
- Confirm email/notifications are working if the module uses `mail.thread`

### First week
- Monitor query performance under real load
- Check for any user-reported issues
- Verify translations are displaying correctly for Spanish users

---

## Migration Script Protocol

When a Major or schema-affecting Minor bump is required:

```
migrations/
└── 19.0.X.Y.0/
    ├── pre-migration.py    # Runs BEFORE module update (schema prep)
    └── post-migration.py   # Runs AFTER module update (data backfill)
```

```python
# post-migration.py template
def migrate(cr, version):
    """Backfill new_field on dipl_model_name after module update."""
    cr.execute("""
        UPDATE dipl_model_name
        SET new_field = default_value
        WHERE new_field IS NULL
    """)
```

Always test migration scripts on a staging database cloned from production before deploying.

---

## CHANGELOG.md Standard

Every maintenance action must be documented:

```markdown
## [19.0.1.2.1] - YYYY-MM-DD

### Fixed
- Root cause description (1 line). Fix: what was changed (1 line).

## [19.0.1.2.0] - YYYY-MM-DD

### Added
- New feature description.

### Changed
- What behavior changed and why.
```

---

## Adaptability: Rare Maintenance Scenarios

| Scenario | Response |
|---|---|
| DB corrupted after deploy | Restore from last Odoo.sh snapshot immediately; diagnose after |
| Migration script fails mid-deploy | Revert merge; fix migration in staging; re-deploy |
| Performance regression post-deploy | `/perf-check` on affected methods; patch release |
| Security vulnerability found | Treat as production-critical hotfix — `/hotfix` immediately |
| Third-party OCA dependency outdated | Pin to working commit; test on staging before bumping |
