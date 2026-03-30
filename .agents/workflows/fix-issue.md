---
description: Corrige un issue o bug siguiendo las convenciones del repositorio.
---
# Fix Issue Workflow (Odoo 19)

Systematic 6-step process to diagnose and fix bugs in custom Odoo modules.

The argument `$ARGUMENTS` contains the bug description or error message.

## When to use this workflow vs `/hotfix`

| Scenario | Workflow |
|---|---|
| Bug found in development or staging | `/fix-issue` (this workflow) |
| Bug affecting production, needs same-day fix | `/hotfix` |

---

## Step 1 — Capture the error

1. Get the full error message and stack trace (Odoo logs, Odoo.sh dashboard, or user report).
2. Identify the error type:
   - **Python exception**: `ValidationError`, `UserError`, `AccessError`, `KeyError`
   - **XML load error**: `ValueError`, missing `inherit_id`, duplicate XML ID
   - **Database error**: `UniqueViolation`, `ForeignKeyViolation`
   - **UI error**: JS console, OWL rendering failure, broken QWeb template
3. Note the exact user action that triggers the error — never assume.

## Step 2 — Identify the trigger path

| Code path | When to suspect |
|---|---|
| Model method (`write`, `create`, `unlink`, `action_*`) | Error on save or button click |
| Computed field | Error appears after changing a related field |
| Constraint (`@api.constrains`, `models.Constraint`) | Error on save with "constraint" in message |
| Controller (HTTP route) | Error via URL request or API call |
| Scheduled action (cron) | Error in server logs at a fixed time |
| XML data load | Error on module install/update |

Consult `odoo-19` skill for ORM method signatures and known failure patterns.

## Step 3 — Isolate the failure location

Search the codebase systematically:

```bash
# Search for the exact error message
grep -r "ExactErrorMessage" . --include="*.py" -l

# Find the method where it fails
grep -r "method_name" . --include="*.py" -n

# For XML data load errors
grep -r "xml_id_here" . --include="*.xml" -n
```

If the error originates in a standard Odoo module, check `src/` **before** modifying any custom code.

## Step 4 — Propose a fix (Propose-First — mandatory)

Present:
- **Root cause**: what exactly causes the bug and why.
- **Files to change**: `[MODIFY]` with full paths.
- **Proposed fix**: minimal change — do not refactor unrelated code.
- **Risk**: could this fix break another behavior?

**WAIT FOR USER APPROVAL.**

## Step 5 — Apply and verify

1. Implement the minimal fix.
2. Run existing tests for the affected module:
   ```bash
   python odoo-bin -t -d test_db --test-tags=/dipl_module_name
   ```
3. Check for regressions — grep all usages of the changed method/field.
4. If the fix changes a `store=True` field or model structure → a migration script is required.

## Step 6 — Document

Update `CHANGELOG.md` under `Fixed`:
- Root cause (1 line)
- Fix applied (1 line)
- Test added (what now covers this scenario)
- Prevention recommendation

---

## Odoo-specific edge cases

| Error type | Most common cause | Where to look |
|---|---|---|
| `ir.model.access` Access Error | Missing ACL entry for new model | `security/ir.model.access.csv` |
| `ValueError` on module install | Invalid XML | XML file in `__manifest__.py` data list |
| `UniqueViolation` | Duplicate XML ID or broken DB constraint | `models.Constraint` definition |
| `KeyError` on field | Field deleted but still referenced | `grep -r "field_name" . --include="*.py" --include="*.xml"` |
| Computed field loop | Circular `@api.depends` chain | Map the full dependency graph |
| `MissingError` | Record deleted, Many2one without `ondelete` | Check `ondelete=` on the relational field |

---

## Principles

- **Minimal change**: do not refactor code that is not broken.
- **Single root cause**: fix the cause, not a symptom.
- **No fallbacks**: one clear code path — never mask errors with bare `try/except`.
- **No assumptions**: if the bug cannot be reproduced, request more context first.
