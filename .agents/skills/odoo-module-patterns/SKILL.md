---
name: odoo-module-patterns
description: >-
  Architectural decision guides for Odoo modules: when to extend vs create,
  ERD, technical decisions, and common design patterns. Use when planning
  new features or modules.
---

# Odoo Module Patterns - Master Index

Architectural guidance for Odoo 19 module design. Read the relevant reference before proposing any model or structure change.

## Decision Guides

| Topic | File | When to Use |
|---|---|---|
| Inheritance | `references/extend-vs-create.md` | Choosing between `_inherit`, `_inherits`, mixin, or new model |
| Dependencies | `references/module-dependencies.md` | Managing relations between custom / standard modules |
| Data Models | `references/data-model-patterns.md` | State machines, parent-child lines, multi-company fields |
| UI Patterns | `references/ui-patterns.md` | Wizards, smart buttons, chatter, search customization |
| Performance | `references/performance-patterns.md` | N+1 prevention, stored compute decisions, bulk ops |

## Code Templates (copy & adapt)

| Template | File | Use for |
|---|---|---|
| New Model | `references/model-pattern.md` | Base model with fields, compute, constraints, actions |
| Model Inheritance | `references/inherit-pattern.md` | Extending standard Odoo models (`res.partner`, etc.) |
| Wizard | `references/wizard-pattern.md` | TransientModel + form view + ACL entry |
| Views (XML) | `references/view-pattern.md` | Form, list, search, action and menuitem |
| Tests | `references/test-pattern.md` | TransactionCase with setUpClass and coverage priorities |
| Controller | `references/controller-pattern.md` | HTTP/JSON endpoints and file download routes |


## How to use these guides

1. **Start with `extend-vs-create.md`** when designing a new feature — it determines the structural approach before any code is written.
2. **Combine guides when needed**: a new model that has a wizard UI requires both `data-model-patterns` and `ui-patterns`.
3. **Reference `performance-patterns.md` on every model** with computed fields or search-heavy usage.
4. When none of the standard patterns fit, escalate: describe the situation and ask before inventing a new pattern.

## Core Principles (Dipleg)

- **Minimalism**: No field, method, or view unless it solves a real business need.
- **Traceability**: Use `mail.thread` + `mail.activity.mixin` for all main business objects.
- **Multi-company by default**: Include `company_id` if the model has any financial or inventory impact.
- **Batch-first**: Every Python method must handle a recordset of N records, not just one.

> For module folder structure and scaffolding, use `/scaffold-module`.
