---
trigger:
globs: "modules/**/*.py", "modules/**/*.xml", "**/*.py", "**/*.xml"
description: Odoo 19 conventions for custom modules
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
