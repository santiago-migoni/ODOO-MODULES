---
trigger:
globs: "modules/**/*.py", "modules/**/*.xml", "modules/**/i18n/**"
description: Quality gates (tests, security, performance)
---

# quality-gates

Quality gates are mandatory.

Before considering the task complete:

- Tests: add/adjust `TransactionCase` / `HttpCase` for any behavior change (computed fields, constraints, state transitions, wizards actions, and access rules).
- Security: ensure ACL/record rules, auth, and no secret leakage (no hardcoded tokens/keys).
- Performance: avoid N+1 and expensive loops; use batching and ORM-friendly patterns.
- Consistency: follow the same coding style already present in the repository and Odoo 19 best practices.
