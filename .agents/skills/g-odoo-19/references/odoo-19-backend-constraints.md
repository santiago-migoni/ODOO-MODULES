# Backend Constraints (Python / ORM)

Rules for writing Odoo 19 server-side Python code. These apply whenever you create or modify models, controllers, or business logic.

## MUST DO

- **Recordset discipline**: Use `self.ensure_one()` for singleton operations. Use `filtered()`, `mapped()`, `sorted()` for recordset manipulation — never iterate with index access.
- **Type hints**: Use `X | False` when returning potentially empty single records (Odoo returns `False`, not `None`, for empty relational fields).
- **Private methods**: Prefix custom business logic methods with `_` (e.g., `_compute_total`, `_check_validity`). Public methods are reserved for actions callable from XML/UI.
- **Computed fields**: Always declare ALL `@api.depends` paths including deep relational routes (e.g., `line_ids.price_unit`). Prefer over-declaring (superfluous recalculations) over under-declaring (silent stale values). Stored computed fields (`store=True`) that need editing MUST define `inverse`. Those needing filtering MUST define `search`.
- **Batch operations**: Use `create([{...}, {...}])` over `create()` inside loops. Use `read_group()` for aggregation instead of iterating + summing.
- **Delete prevention**: Use `@api.ondelete(at_uninstall=False)` — not `unlink()` overrides.
- **SQL constraints**: Use `models.Constraint` — not legacy `_sql_constraints`.
- **Model metadata**: Define `_description` for every new model. Use `_rec_name` or `_compute_display_name` for display (not legacy `name_get`).
- **Logging**: Use `_logger = logging.getLogger(__name__)` at module level. Use `_logger.info()`, `_logger.warning()`, `_logger.error()`.
- **Security**: Every new model MUST have `ir.model.access.csv` entries before first test. `sudo()` usage MUST be justified and reviewed.
- **Polymorphic links**: Use `fields.Reference` with `selection` via lambda for dynamic options — avoids proliferation of redundant Many2one fields.
- **Many2many with metadata**: When a relationship needs additional data (dates, status), define explicit intermediate table or materialize as full `models.Model`.

## MUST NOT DO

- **NEVER** use `async/await` inside Odoo models — the ORM is synchronous.
- **NEVER** use `cr.execute()` unless strictly necessary for raw performance, and always use parameterized queries (`%s` placeholders) to prevent SQL injection.
- **NEVER** use `fields.Date.today()` as a field default — use `fields.Date.context_today` (respects user timezone).
- **NEVER** use `search()` inside loops — causes N+1 queries. Batch with domains or use `read_group()`.
- **NEVER** skip security definitions for new models — missing ACL = `AccessError` on install.
- **NEVER** use `eval()` or `exec()` with user-supplied data.
- **NEVER** hardcode credentials, tokens, or secrets in code.
- **NEVER** use deprecated patterns: `attrs={}` (use direct `invisible=`), `<tree>` (use `<list>`), `group_operator=` (use `aggregator=`), `_sql_constraints` (use `models.Constraint`).

## Inheritance Quick Reference

| Type | Syntax | DB Impact | Use Case |
|---|---|---|---|
| Extension | `_inherit = 'model'` (no `_name`) | Adds columns to existing table | Add fields/behavior to standard models |
| Classical | `_name = 'new'` + `_inherit = 'parent'` | New table, copies all columns | Independent entity similar to parent |
| Delegation | `_inherits = {'parent': 'field_id'}` | FK-linked tables (composition) | Normalized schema, no data duplication |

See rule `06-inheritance-strategy` for detailed decision guide.
