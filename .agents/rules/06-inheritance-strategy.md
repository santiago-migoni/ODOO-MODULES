---
trigger:
globs: "**/*.py"
phase: f3
description: Mandatory inheritance decision before coding any model
---

# inheritance-strategy

Before defining or extending any model, you MUST choose the correct inheritance paradigm. This decision has irreversible implications on database performance and long-term maintenance costs.

## Three Paradigms

| Type | Syntax | DB Structure | When to Use |
|---|---|---|---|
| Extension | `_inherit = 'model.name'` (no `_name`) | Single Table — columns added to existing table | Inject fields, override methods, alter behavior on an existing entity (e.g., loyalty points on `res.partner`). Most common pattern. |
| Classical | `_name = 'new.model'` + `_inherit = 'parent.model'` | New separate table with copies of all parent columns | New entity conceptually similar to parent but needs its own identity, ACL, and sequences (e.g., `supplier` inheriting from contact). Use sparingly — duplicates schema. |
| Delegation | `_inherits = {'parent.model': 'field_id'}` + `Many2one` field | Multiple tables linked by Foreign Keys (composition) | Avoid data duplication. New entity transparently accesses parent fields. Structural pattern: `res.users` → `res.partner`, `product.product` → `product.template`. Prefer for normalization. |

## Rules

- **Document the choice** in the proposal (Fase 3) with rationale.
- **Prefer Extension** for adding fields/behavior to standard models.
- **Prefer Delegation** over Classical when the new entity shares data with a parent — it normalizes the schema and prevents bloated tables.
- **Classical inheritance creates full column copies** — only use when the new entity truly needs independent storage.
- **Wrong choice = expensive refactoring**. Changing inheritance type after production deployment requires migration scripts and potential data loss.

## Checklist (before coding)

- [ ] Identified whether this is an extension of an existing model or a new entity.
- [ ] If new entity: evaluated Delegation vs Classical based on data overlap.
- [ ] Documented the inheritance decision in the technical proposal.
- [ ] Confirmed no N+1 implications from delegation JOINs on high-traffic models.
