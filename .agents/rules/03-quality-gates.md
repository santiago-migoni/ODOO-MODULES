---
trigger:
globs: "modules/**/*.py", "modules/**/*.xml", "modules/**/i18n/**"
description: Quality gates (tests, security, performance)
phase: f5
---

# quality-gates

Quality gates are mandatory.

Before considering the task complete:

- Tests: add/adjust `TransactionCase` / `HttpCase` for any behavior change (computed fields, constraints, state transitions, wizards actions, and access rules).
- Security: ensure ACL/record rules, auth, and no secret leakage (no hardcoded tokens/keys).
- Performance: avoid N+1 and expensive loops; use batching and ORM-friendly patterns.
- Consistency: follow the same coding style already present in the repository and Odoo 19 best practices.

## Testing Methods (by priority)

- **Form helper**: Preferred method for testing model behavior that involves UI interaction. Emulates `@api.onchange` triggers and default propagation — higher fidelity than direct `write()` calls.
- **HOOT framework**: For JavaScript/OWL component testing. Use `mountWithCleanup`, `mountView`, and `expect` assertions. Mock RPC calls to isolate component behavior.
- **Tours (E2E)**: End-to-end integration tests via `tour.register`. Test the full Python ↔ JavaScript bridge. Structure in logical steps: locate trigger in DOM → wait for async confirmation → execute interaction. Tours serve dual purpose: regression prevention AND executable business specifications.

## QA Pyramid (5 levels)

1. Unit tests — `TransactionCase` (computed fields, constraints, state flows, CRUD, permissions)
2. Integration tests — `HttpCase` (controllers, portal flows)
3. Performance audit — `/perf-check` (N+1, indexes, query count)
4. Security audit — `/security-audit` (ACL, record rules, sudo, SQL injection)
5. Manual smoke test — End-to-end with real data on staging
