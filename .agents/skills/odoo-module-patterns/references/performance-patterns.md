# Performance Patterns Guide

Odoo 19 performance patterns focused on ORM usage. For framework-level detail, consult `odoo-19/references/odoo-19-performance-guide.md`.

## 1. Avoid N+1 Queries

Never call `search()` or `browse()` inside a loop.

```python
# BAD — N+1: one query per partner
for partner in partners:
    orders = self.env["sale.order"].search([("partner_id", "=", partner.id)])

# GOOD — single query for all partners
orders = self.env["sale.order"].search([("partner_id", "in", partners.ids)])
```

Use `read_group()` for aggregations instead of search + loop:
```python
# GOOD — one SQL query for counts
data = self.env["sale.order"].read_group(
    domain=[("state", "=", "sale")],
    fields=["partner_id", "amount_total:sum"],
    groupby=["partner_id"],
)
```

## 2. Computed Fields — Store Decision

| Scenario | Use `store=True` | Use `store=False` |
|---|---|---|
| Field appears in list view | ✅ | ❌ (recalculates per row) |
| Field used in `search()` domain | ✅ | ❌ (not searchable) |
| Value changes on every write | ❌ | ✅ |
| Only for display in form | Optional | ✅ |

Always verify `@api.depends` targets only the minimum necessary fields to avoid excessive recomputation.

## 3. Indexing (`index=True`)

Apply to fields used in:
- `search()` / `filtered_domain()` domains.
- `order` clauses in list views.
- All `Many2one` relation fields (Odoo default for relational fields, but always explicit for custom ones).

## 4. SQL Constraints vs Python Constraints

Prefer `models.Constraint` (SQL-level) when the rule is expressible in SQL — it runs in the DB engine and bypasses ORM overhead. Use `@api.constrains` only for cross-model logic or Python-only conditions.

## 5. Large Data Migrations

When processing thousands of records (e.g., in a `post-migration.py` script):
- Use `env.cr.execute()` with parameterized queries for bulk updates.
- Process in batches of 1000 records with `env.cr.commit()` between batches to avoid lock timeouts.
- Disable computed field recomputation with `env = env(context={"recompute": False})` when safe.
