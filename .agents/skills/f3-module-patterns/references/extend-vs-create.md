# Extend vs Create Guide

Decision tree for choosing the right inheritance pattern in Odoo 19.

## 1. Inheritance Options

### Traditional Inheritance (`_inherit`)
Add fields/methods to an existing Odoo or custom model.
- **When**: You need to modify a standard behavior (e.g., add a field to `res.partner`).
- **Effect**: Changes the DB table directly.

### Prototype Inheritance (`_inherit` without `_name`)
Same as traditional, but for custom models.
- **When**: You need to apply business logic to multiple of your own models.

### Delegation Inheritance (`_inherits`)
Link one model to another (composition).
- **When**: You want to "be" something else without sharing the table (e.g., `res.users` inherits `res.partner`).

## 2. Decision Matrix

| Requirement | Preferred Pattern | Example |
|---|---|---|
| Modification of Odoo base (CRM, Sales, etc.) | `_inherit` | Add `vat_2` to `res.partner` |
| New business concept with its own life | **New Model** | `dipl.shipment.plan` |
| Multiple models sharing logic (e.g., tracking) | **Mixin** | `mail.thread` |
| Entity with different roles | `_inherits` | `hospital.doctor` inherits `res.partner` |

## 3. Best Practices

1. **Avoid Over-Inheritance**: If you're adding 20+ fields to a standard model, it might be better as a separate model with a `Many2one`.
2. **Naming**: Custom models always prefixed with `dipl_`.
3. **Logic Flow**: When using `_inherit`, always `super()` unless you intentionally want to override standard behavior completely (rare/risky).
