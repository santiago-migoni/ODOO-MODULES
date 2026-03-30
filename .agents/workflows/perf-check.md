---
description: Realiza una auditoría de performance N+1 en un módulo de Odoo 19.
---
# Performance Check Workflow

Process to audit the performance of a custom Odoo 19 module.

The argument `$ARGUMENTS` contains the target module name.

## 1. Analysis Phase

1. Scan for `search()` or `browse()` inside loops (`for record in records:`).
2. Check for `@api.depends` that trigger too often or on broad fields.
3. Review `Many2one` relations for missing `index=True`.
4. Identify computed fields that aren't stored but are used in list views.

## 2. Findings

Categorize issues:
- **Critical**: N+1 queries in high-usage methods.
- **High**: Misconfigured `@api.depends` causing unnecessary re-computes.
- **Medium**: Missing indexes on search/filter fields.
- **Info**: Suggestions for `read_group()` vs `search()`.

## 3. Recommended Fixes

- Convert loops into recordset operations.
- Use `mapped()` or `filtered()` when logical.
- Add `index=True` for performance-critical fields.
- Set `store=True` for computed fields in large tables.

## 4. Verification

1. Use `Query Count` assertions in tests (if supported).
2. Measure response time before and after the fix.
3. Verify that the logic remains correct after optimization.
4. Update `GEMINI.md` performance section if new patterns are identified.
