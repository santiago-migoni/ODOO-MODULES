---
description: Proceso para agregar nuevas funcionalidades a módulos existentes en Odoo 19.
---
# New Feature Workflow

Step-by-step guide to add a new feature to an existing Odoo 19 module.

The argument `$ARGUMENTS` contains the target module name and a brief feature description.

## 1. Analysis phase

1. Locate the module: `find . -maxdepth 2 -name "__manifest__.py" | xargs grep -l "{module_name}"`. Custom modules live at the repo root — not inside `src/` (that folder is Odoo source reference only).
2. Read the module's `__manifest__.py` to understand dependencies and data file load order.
3. Read existing `models/` files to map current fields, methods, and state machines.
4. Consult **`odoo-module-patterns`** skill:
    - `extend-vs-create.md` — decide if the feature needs a new model or extends an existing one.
    - `data-model-patterns.md` — if state machine or parent-child lines are involved.
    - `ui-patterns.md` — if wizard, smart button, or chatter interaction is needed.

## 2. Proposal (Propose-First)

Present using the standard proposal format from `GEMINI.md`:
- **Goal**: the business problem being solved.
- **Plan**: ordered implementation steps.
- **Files**: `[NEW]` / `[MODIFY]` / `[DELETE]` with full paths.
- **Tests**: what `TransactionCase` / `HttpCase` coverage will be added.
- **Risks**: assumptions, upstream module changes, migration needs.

**WAIT FOR USER APPROVAL.**

## 3. Implementation order

Always implement in dependency order to avoid broken intermediate states:
1. Python models (fields, methods, constraints).
2. Security (`ir.model.access.csv`, record rules if new model).
3. XML views (form, list, search, menus).
4. Tests (`/generate-tests` — **mandatory**, not optional).
5. Translations (`/translate` — **mandatory**, not optional).

## 4. Edge cases

- **Multi-module feature**: If the feature touches more than one module, create a separate branch per module and merge in dependency order. Note inter-module XML ID references to avoid load order errors.
- **Upstream dependency change**: If the feature requires adding to `depends`, re-run `/security-audit` after — new model access may need new ACL entries.
- **Inherited model conflict**: If a field name you need already exists in the inherited model, use `_compute` override or a prefixed name (`dipl_field_name`) to avoid collision.
