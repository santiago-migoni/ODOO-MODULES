---
description: Captura y valida los requisitos de un módulo Odoo antes de escribir código.
---

> **Fase**: F1 — Planificación
> **Dónde estamos**: Se ha identificado una necesidad de negocio. Necesitamos validarla antes de diseñar.
> **Por qué esta fase**: Sin validación formal, el desarrollo arranca sobre supuestos. El GAP Analysis previene scope creep y alinea expectativas con el SPoC.
> **Habilita**: Fase 2 (Análisis) — produce un backlog priorizado que el análisis técnico consumirá.

# Plan Module Workflow (Fase 1 — Planificación y Requisitos)

Structured requirements capture for a new Odoo module or significant feature.
Run this workflow before `/scaffold-module` or `/new-feature`.

The argument `$ARGUMENTS` contains a brief description of the business need.

---

## Step 1 — Define the business problem

Answer in one paragraph:
- **What pain does it solve?** (not what it does — why does it matter)
- **Who is the user?** (internal user, manager, portal user, external API)
- **What is the success condition?** (how will we know it works?)

Document in `docs/requirements/{module_name}.md`.

## Step 2 — Determine the work type

| Type | When | First workflow to use |
|---|---|---|
| New standalone module | New business object, no Odoo standard model fits | `/scaffold-module` |
| Extension of existing module | Adding fields/logic to `sale.order`, `res.partner`, etc. | `/new-feature` |
| Wizard only | One-time action or bulk operation | `/add-wizard` |
| Report only | PDF or HTML output from existing data | `/add-report` |

## Step 3 — Odoo-specific requirements capture

Ask and document answers to all of these:

| Question | Default if unknown | Impact |
|---|---|---|
| What Odoo standard models are involved? | Ask before assuming | Determines `depends` list |
| Is this module already in production? | Assume no | Yes → migration scripts required for model changes |
| Does data have financial or inventory impact? | Assume no | Yes → `company_id` + multi-company record rule mandatory |
| Does it depend on an OCA module? | Assume no | Yes → git submodule required before starting |
| Does it need portal user access? | Assume no | Yes → `auth="user"` controllers + portal record rules |
| Does it need scheduled processing? | Assume no | Yes → `ir.cron` action in data files |
| Does it need email notifications? | Assume no | Yes → `mail.thread` + `mail.activity.mixin` on main model |

If any answer is uncertain, **ask the user** — never invent identifiers or business rules.

## Step 4 — Viability check

Before proceeding, confirm:
- [ ] No existing `dipl_*` module already solves this (run `grep -r "keyword" . --include="*.py"`)
- [ ] No OCA community module covers this need (check before building custom)
- [ ] The `depends` list is available in the target Odoo.sh environment

If viability is uncertain, **stop here and escalate** — do not design a module that cannot be deployed.

## Step 5 — Estimate with scrum-master skill

Invoke `scrum-master` to:
1. Break the requirement into stories (1–3 days each, max 8 story points)
2. Estimate sprint capacity needed
3. Identify blockers and dependencies between stories

Output: `docs/stories/{module_name}-sprint-plan.md`

## Step 6 — Go / No-Go decision

Present a summary to the user:

```
## Plan Summary — {module_name}

**Business problem:** [1 sentence]
**Work type:** [New module / Extension / Wizard / Report]
**Estimated stories:** [N stories, ~X story points, ~Y days]
**Key dependencies:** [list of Odoo modules, OCA deps, other dipl_ modules]
**Risks/assumptions:** [list]

Decision: GO → proceed to Fase 2 (Análisis) or Fase 3 (Diseño)
          NO-GO → reason and recommendation
```

**WAIT FOR USER APPROVAL before proceeding to the next phase.**

## GAP Analysis (paso formal)

Antes de crear el backlog, ejecutar un análisis de brechas:

1. **Comparar** la necesidad con funcionalidades nativas de Odoo.
2. **Clasificar** la brecha: ¿configuración, extensión de modelo existente, o módulo nuevo?
3. **Justificar** técnica y financieramente el desarrollo custom (si aplica).
4. **Documentar** dependencias lógicas entre este requerimiento y otros módulos.
5. **Generar** el backlog priorizado respetando dependencias (ej: inventario avanzado necesita maestro de productos).

Referencia: skill `f0-enterprise-sdlc` para metodología completa de GAP Analysis.
