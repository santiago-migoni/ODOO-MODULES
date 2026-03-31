---
name: odoo-analysis
description: >-
  Analysis skill for mapping existing Odoo code before designing changes.
  Use at Fase 2 (Analysis) when starting any feature or fix on an existing
  module: maps models, views, security, dependencies and logic before writing
  any code. Activate with keywords: analyze module, map models, understand
  code, existing module structure, dependencies, before designing.
---

# Odoo Analysis Skill

**Role:** Fase 2 — Analysis specialist for Odoo 19 modules

**Activate when:** A feature or fix requires understanding code that already exists — in a custom `dipl_` module or in Odoo standard (`src/`).

## Lean Principle

> Analyze only what is strictly necessary to answer the design question. Stop when the question is answered — over-analysis is waste (muda).

---

## Analysis Process (in order)

### 1. Module map

```bash
# Locate the module
find . -maxdepth 2 -name '__manifest__.py' | xargs grep -l "module_name"
```

Read `__manifest__.py`:
- `depends` → what Odoo modules are required
- `data` → load order of security/views/data files
- `version` → whether migration scripts may exist in `migrations/`

### 2. Model map

For each file in `models/`:
- `_name` → technical model name (maps to DB table `model_name` → `model_name` replacing dots with underscores)
- `_inherit` / `_inherits` → what it extends
- Fields: type, `store=`, `compute=`, `related=`, `index=`
- State machine: `state` field with `Selection` values and valid transitions
- Key methods: `create`, `write`, `unlink` overrides, `action_*` methods

### 3. View map

For each file in `views/`:
- Which model each view targets (`model=`)
- Fields exposed in form / list / search views
- Groups (`groups=`) restricting visibility
- `inherit_id` → does this view extend a standard Odoo view?

### 4. Security map

- `security/ir.model.access.csv` → who can CRUD each model
- `security/security.xml` → groups defined, record rules active
- Multi-company: does any model have `company_id` with a record rule?

### 5. Logic map

- Computed fields: `@api.depends` chain — what triggers re-computation and at what cost
- Constraints: `@api.constrains` — what invariants are enforced
- Delete prevention: `@api.ondelete`
- External calls: `@api.model` methods callable from outside

### 6. Impact analysis

Before proposing any change, answer:
- What other `dipl_*` modules reference this module via XML IDs?
- What standard Odoo views does this module extend?
- If a field is removed/renamed, which views, methods, and reports break?

```bash
# Find all cross-module XML ID references
grep -r "module_name\." . --include="*.xml" -l

# Find all field usages across the project
grep -r "field_name" . --include="*.py" --include="*.xml" -n
```

---

## Standard Odoo Reference

When analyzing standard models, use `src/` as reference:
- `src/odoo/addons/{module}/models/` for Python
- `src/odoo/addons/{module}/views/` for XML

Never modify files inside `src/` — it is read-only reference.

---

## Output format

After completing the analysis, always produce this summary before proposing any changes:

```
## Analysis Summary — {module_name}

**Models analyzed:** [list with _name]
**Views analyzed:** [form/list/search for each model]
**Security impact:** [yes/no — describe groups/ACL affected]
**Migration needed:** [yes/no — reason: new store field / model rename / etc.]
**Cross-module dependencies:** [list of dipl_* modules that reference this code]
**Key risks:** [list of things that could break]
```

This output is mandatory input for Fase 3 (Diseño) — do not skip it.
