---
trigger:
globs: "modules/**/*.py", "modules/**/*.xml", "**/*.py", "**/*.xml"
description: Odoo 19 conventions for custom modules
phase: f4
---

# odoo-19-conventions

Odoo 19 conventions are mandatory for all custom modules.

Checklist (must pass before marking work as done):

- Use `<list>` (not `<tree>`).
- Use direct UI attributes (e.g. `invisible="..."`) instead of legacy `attrs="..."` patterns.
- Use delete prevention via `@api.ondelete(at_uninstall=False)` (avoid `unlink()` validation overrides).
- Use `aggregator=` for grouped fields (not `group_operator=`).
- Prefer batch operations (`create([{...}, {...}])`) over `create()` inside loops.
- Avoid N+1: never `search()` inside loops; use batched domains, `read_group()`, or aggregated queries.
- Computed fields: declare ALL dependencies in `@api.depends`, including deep relational paths (e.g., `line_ids.price_unit`). Prefer over-declaring (superfluous recalculations) over under-declaring (silent stale values).
- Stored computed fields (`store=True`) that need to be editable MUST define an `inverse` method. If they need to be searchable/filterable, MUST define a `search` method.
- Use `fields.Reference` for polymorphic links (one field linking to multiple model types). Define `selection` via lambda for dynamic options.
- Use explicit intermediate table definitions for `Many2many` fields when the relationship requires metadata (dates, status, comments). Materialize as a full `models.Model` when needed.
- Use `models.Constraint` for SQL constraints (not legacy `_sql_constraints`).
