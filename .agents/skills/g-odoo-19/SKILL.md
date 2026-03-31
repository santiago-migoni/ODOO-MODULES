---
name: odoo-19
description: >-
  Odoo 19 development knowledge base with 22 specialized references covering
  the complete stack: ORM/backend, XML views, OWL frontend, themes/SCSS,
  actions, controllers, fields, decorators, mixins, migration, performance,
  security, testing, transactions, translations, and QWeb reports.
  Use when writing, reviewing, or debugging any Odoo 19 code.
---

# Odoo 19 Skill — Master Index

Load the appropriate reference from `references/` based on your task. Do NOT load all references at once — pick only what you need.

## Implementation Constraints

| Domain | Reference | Load When |
|--------|-----------|-----------|
| Backend / ORM | `references/odoo-19-backend-constraints.md` | Writing models, computed fields, security, batch ops, inheritance |
| Views / XML | `references/odoo-19-view-constraints.md` | Writing Form, List, Kanban, Pivot, Search views, XPath inheritance |
| OWL / JS | `references/odoo-19-owl-constraints.md` | Building OWL components, hooks, services, patch(), registry |
| Theme / SCSS | `references/odoo-19-theme-constraints.md` | SCSS, Bootstrap overrides, website snippets, QWeb reports, print CSS |

## API & Framework Guides

| Topic | Reference | Load When |
|-------|-----------|-----------|
| Actions | `references/odoo-19-actions-guide.md` | Creating actions, menus, scheduled jobs, server actions |
| API Decorators | `references/odoo-19-decorator-guide.md` | @api.depends, @api.constrains, @api.ondelete, @api.onchange |
| Controllers | `references/odoo-19-controller-guide.md` | HTTP endpoints, routes, JSON-RPC, web controllers |
| Data Files | `references/odoo-19-data-guide.md` | XML/CSV data files, records, noupdate, shortcuts |
| Development | `references/odoo-19-development-guide.md` | Module creation, manifest, wizards, reports overview |
| Field Types | `references/odoo-19-field-guide.md` | Defining fields, choosing field types, parameters |
| Manifest | `references/odoo-19-manifest-guide.md` | __manifest__.py, dependencies, assets, hooks |
| Migration | `references/odoo-19-migration-guide.md` | Upgrade scripts, data migration, pre/post hooks |
| Mixins | `references/odoo-19-mixins-guide.md` | mail.thread, activities, email aliases, tracking |
| Model Methods | `references/odoo-19-model-guide.md` | ORM queries, CRUD, domain filters, recordsets |
| OWL Guide | `references/odoo-19-owl-guide.md` | OWL components deep dive, hooks, services |
| Performance | `references/odoo-19-performance-guide.md` | N+1 prevention, batch ops, query optimization |
| Reports | `references/odoo-19-reports-guide.md` | QWeb reports, PDF/HTML, paper formats, barcodes |
| Security | `references/odoo-19-security-guide.md` | Access rights, record rules, field permissions |
| Testing | `references/odoo-19-testing-guide.md` | TransactionCase, HttpCase, mocking, HOOT, Tours |
| Transactions | `references/odoo-19-transaction-guide.md` | Savepoints, UniqueViolation, serialization failures |
| Translation | `references/odoo-19-translation-guide.md` | i18n, PO files, translatable fields |
| Views & XML | `references/odoo-19-view-guide.md` | XML views, actions, menus, QWeb templates |

## File Structure

```
skills/g-odoo-19/
├── SKILL.md                                # This file — master index
└── references/                             # 22 specialized references
    ├── odoo-19-backend-constraints.md      # MUST DO / MUST NOT DO for Python/ORM
    ├── odoo-19-view-constraints.md         # MUST DO / MUST NOT DO for XML/views
    ├── odoo-19-owl-constraints.md          # MUST DO / MUST NOT DO for OWL/JS
    ├── odoo-19-theme-constraints.md        # MUST DO / MUST NOT DO for SCSS/themes/reports
    ├── odoo-19-actions-guide.md
    ├── odoo-19-controller-guide.md
    ├── odoo-19-data-guide.md
    ├── odoo-19-decorator-guide.md
    ├── odoo-19-development-guide.md
    ├── odoo-19-field-guide.md
    ├── odoo-19-manifest-guide.md
    ├── odoo-19-migration-guide.md
    ├── odoo-19-mixins-guide.md
    ├── odoo-19-model-guide.md
    ├── odoo-19-owl-guide.md
    ├── odoo-19-performance-guide.md
    ├── odoo-19-reports-guide.md
    ├── odoo-19-security-guide.md
    ├── odoo-19-testing-guide.md
    ├── odoo-19-transaction-guide.md
    ├── odoo-19-translation-guide.md
    └── odoo-19-view-guide.md
```

## Base Code Reference (Odoo 19)

All guides are based on analysis of Odoo 19 source code:

- `odoo/models.py` — ORM implementation
- `odoo/fields.py` — Field types
- `odoo/api.py` — Decorators
- `odoo/http.py` — HTTP layer
- `odoo/exceptions.py` — Exception types
- `odoo/tools/translate.py` — Translation system
- `addons/web/static/src/core/` — OWL components and services

## External Documentation

- [Odoo 19 Official Documentation](https://github.com/odoo/documentation/tree/19.0)
- [Odoo 19 Developer Reference](https://github.com/odoo/documentation/blob/19.0/developer/reference/orm.rst)
