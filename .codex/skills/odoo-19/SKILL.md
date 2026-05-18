---
name: odoo-19
description: >-
  Odoo 19 development knowledge base with specialized references covering the
  complete stack: ORM/backend, XML views, OWL frontend, themes/SCSS, actions,
  controllers, fields, decorators, mixins, migration, performance, security,
  testing, transactions, translations, and QWeb reports. Use when writing,
  reviewing, or debugging any Odoo 19 code.
---

# Odoo 19

## Overview
Use this skill as the transversal technical reference across `odoo-analysis-planning`, `odoo-design`, `odoo-coding`, `odoo-testing`, `odoo-deployment`, and `odoo-maintenance`.
Load only the specific reference needed for the current task. Do not load the full reference set by default.

## Required Inputs
- The concrete technical question or implementation area.
- The active delivery stage or immediate engineering task.

## Workflow
1. Identify the technical domain involved in the current task.
2. Load only the matching reference file from `references/`.
3. Apply the referenced constraints and guidance to the active operational skill.
4. Return to the calling skill with the technical decision or implementation guidance.

## Reference Index

| Domain | Reference | Load When |
|--------|-----------|-----------|
| Backend / ORM | `references/odoo-19-backend-constraints.md` | Writing models, computed fields, security, batch ops, inheritance |
| Views / XML | `references/odoo-19-view-constraints.md` | Writing Form, List, Kanban, Pivot, Search views, XPath inheritance |
| OWL / JS | `references/odoo-19-owl-constraints.md` | Building OWL components, hooks, services, patch(), registry |
| Theme / SCSS | `references/odoo-19-theme-constraints.md` | SCSS, Bootstrap overrides, website snippets, QWeb reports, print CSS |
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
| Views And XML | `references/odoo-19-view-guide.md` | XML views, actions, menus, QWeb templates |

## Outputs
- Targeted Odoo 19 technical guidance for the active task.
- Framework constraints that should shape design, coding, testing, deployment, or maintenance decisions.

## Definition of Done
- Only the relevant references were loaded.
- Technical guidance is specific enough to support the active stage without adding unnecessary context.

## Handoff
- Hand off back to the calling operational skill once the technical guidance is clear.
- Prefer `odoo-design` for architecture decisions, `odoo-coding` for implementation, `odoo-testing` for validation depth, `odoo-deployment` for migration-sensitive rollout questions, and `odoo-maintenance` for framework-level incident diagnosis.

## Base Code Reference

All guides are based on analysis of Odoo 19 source code:

- `odoo/models.py` - ORM implementation
- `odoo/fields.py` - Field types
- `odoo/api.py` - Decorators
- `odoo/http.py` - HTTP layer
- `odoo/exceptions.py` - Exception types
- `odoo/tools/translate.py` - Translation system
- `addons/web/static/src/core/` - OWL components and services

## External Documentation

- [Odoo 19 Official Documentation](https://github.com/odoo/documentation/tree/19.0)
- [Odoo 19 Developer Reference](https://github.com/odoo/documentation/blob/19.0/developer/reference/orm.rst)
