---
name: odoo-qa
description: >-
  QA and quality validation specialist for Odoo 19 modules. Use at Fase 5
  (Pruebas / QA) to verify test coverage, performance, security, and
  translations before any deploy. Activate with keywords: test coverage,
  quality gates, validation, QA, before deploy, test the module.
---

> **Fase**: F5 — Pruebas / QA
> **Dónde estamos**: El código está implementado. Antes de desplegar, validamos calidad, rendimiento, seguridad y traducciones.
> **Qué hacer**: Ejecutar la pirámide QA completa (5 niveles), validar quality gates.
> **Cómo hacerlo**: Skill f5-odoo-qa + workflows /generate-tests, /perf-check, /security-audit.
> **Por qué así**: Cada bug detectado en QA cuesta 10x menos que en producción (principio Six Sigma). Sin QA riguroso, la Fase 6 (Deploy) inyecta defectos directamente en la operación corporativa.

# Odoo QA Skill

**Role:** Fase 5 — Quality Assurance specialist for Odoo 19 modules

**Activate when:** A module is ready for testing, before merge to staging or production.

## Six Sigma Principle

> Zero defects before deploy. Every untested behavior is a potential production failure.
> Lean principle: catching a bug in QA costs 10x less than catching it in production.

---

## QA Pyramid for Odoo

Run top-down, but plan bottom-up:

```
Level 5 — Manual smoke test (end-to-end with real data)
Level 4 — Security audit (/security-audit)
Level 3 — Performance audit (/perf-check)
Level 2 — Integration tests (HttpCase — controllers, OWL tours)
Level 1 — Unit tests (TransactionCase — models, constraints, state flows)
```

---

## Level 1 — Unit Tests (mandatory)

Use `/generate-tests` to create `TransactionCase` coverage for:

| Priority | What to test |
|---|---|
| 1 | Computed fields — correct result with different inputs |
| 2 | Constraints — `ValidationError` raised when invariant is violated |
| 3 | State flows — valid transitions succeed, invalid ones raise errors |
| 4 | CRUD overrides — custom `create`, `write`, `unlink` |
| 5 | Permissions — access with different user groups |

**Minimum coverage gate:**
- Every public method with business logic must have at least one test.
- Every `@api.constrains` must have a test that triggers it.
- Every state transition must have a test for the happy path.

## Level 2 — Integration Tests (when applicable)

Use `HttpCase` for:
- HTTP controllers with non-trivial logic
- OWL components with complex user interactions (use tours)
- Portal access flows

## Level 3 — Performance Audit

Run `/perf-check` on the module. Zero tolerance for:
- `search()` or `browse()` inside a `for` loop (N+1)
- `@api.depends` on fields that change too frequently without `store=True`
- Missing `index=True` on `Many2one` fields used in filters or list views

## Level 4 — Security Audit

Run `/security-audit` on the module. Zero tolerance for:
- Any model without an entry in `ir.model.access.csv`
- `sudo()` in a method callable by portal or public users without explicit privilege check
- `eval()` or raw SQL with string interpolation (f-strings in `cr.execute`)
- `t-raw` in QWeb templates (removed in Odoo 19 — use `t-out`)

## Level 5 — Manual Smoke Test

Test the core user flow affected by the module with real (or realistic) data:

1. Install the module on a clean database or staging.
2. Perform the main business action end-to-end.
3. Verify computed fields display correctly in list and form views.
4. Check that permission restrictions work for non-admin users.
5. Verify Spanish translations are present for all UI strings.

---

## Quality Gates Checklist (non-negotiable)

Before any merge to staging or production:

- [ ] **Tests**: All new logic covered by `TransactionCase` or `HttpCase`
- [ ] **Security**: ACL entries exist for all new models; record rules correct
- [ ] **Performance**: No N+1 queries; indexes on filtered fields
- [ ] **Translations**: `i18n/es.po` updated via `/translate` — all msgid present
- [ ] **Consistency**: Code follows Odoo 19 conventions from `GEMINI.md`
- [ ] **CHANGELOG**: Entry added under correct version

---

## What NOT to test

- Trivial field getters/setters with no logic
- Odoo ORM internal behavior (already tested upstream in `src/`)
- Static XML rendering without dynamic logic

---

## Adaptability: Handling Rare QA Scenarios

| Scenario | Response |
|---|---|
| Module has no tests at all | Generate full baseline with `/generate-tests` before QA |
| Performance issue found in audit | Fix before proceeding — do not deploy with known N+1 |
| Security issue found | Block deploy — escalate to `/hotfix` protocol if already in production |
| Translation gap after `/translate` | Re-run `/translate` and commit before merging |
| Manual smoke test fails in staging | Create `fix/` branch and cycle back to Fase 4 |

## Form Helper — Emulación de UI en Tests

La clase `Form` de Odoo emula el comportamiento del cliente web en los tests:
- Al inyectar valores programáticamente, activa `@api.onchange` y propagación de defaults.
- Fidelidad superior a llamadas directas de `write()` al ORM.
- Uso preferido para tests de wizards, formularios y flujos de estado.

```python
from odoo.tests.common import Form

with Form(self.env['dipl.example']) as f:
    f.name = "Test Record"
    f.partner_id = self.partner  # triggers onchange
    record = f.save()
```

## HOOT Framework — Tests de JavaScript/OWL

Framework propio de Odoo para testing de componentes frontend:
- `mountWithCleanup`: Monta componente con limpieza automática.
- `mountView`: Monta una vista completa para testing de integración.
- `expect`: Aserciones deterministas sobre el DOM virtual.
- Mocking de RPC: Intercepta llamadas asíncronas al backend para aislar el componente.

## Tours E2E — Especificaciones Ejecutables

Los Tours (`tour.register`) son scripts interactivos que testean el puente Python ↔ JavaScript:
- Estructurados en pasos lógicos: localizar trigger en DOM → esperar confirmación asíncrona → ejecutar interacción.
- **Dualidad**: Funcionan simultáneamente como anti-regresión Y como especificaciones de negocio documentadas y ejecutables.
- Reemplazan documentación de texto que se vuelve obsoleta rápidamente.
