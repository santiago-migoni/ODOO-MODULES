# Odoo 19 Custom Module Development — Dipleg

This repository contains custom Odoo 19.0 Community modules for Dipleg, deployed on Odoo.sh.

## Language

- Reply and propose in Spanish.
- Code comments: minimal, English, only when helpful.

## Workflow

1. Understand the requirement (ask clarifying questions if needed).
2. Propose a plan and options — **always before coding**.
3. Wait for approval before making edits.
4. Implement with minimal, targeted edits.
5. Add/adjust tests and run a quick sanity check when possible.
6. Final review: correctness, security, performance, Odoo 19 conventions.

### Propose-first rule

Do NOT directly edit files or generate large code changes until you present:
- The intended approach
- The affected files
- The test strategy (at least what to add/check)

Proceed only after approval. If the user has not approved, stop at the proposal stage.

### Proposal format

When proposing changes, always use this structure:

- **Goal**: what problem is being solved and why.
- **Plan**: ordered steps to implement.
- **Files**: explicit list of files to create or modify (with [NEW] / [MODIFY] / [DELETE]).
- **Tests/checks**: what tests to add and what to manually verify.
- **Risks/assumptions**: any uncertainty, dependency, or assumption that requires user confirmation.

Provide 2–3 alternatives only when the user explicitly asks for options.

### Missing context

If critical context is missing (model name, XML IDs, view structure, security groups, business logic intent):

1. Ask **targeted, specific questions** — one question per unknown.
2. If proceeding is necessary, propose a safe default and **clearly mark it as an assumption**.
3. Never invent identifiers (XML IDs, model names, field names) without evidence from the codebase.

## Skill activation guide

| Situation | Use this skill |
|---|---|
| Looking up field types, decorators, ORM methods, views | `odoo-19` |
| Mapping existing module code before designing changes (Fase 2) | `odoo-analysis` |
| Planning module structure, inheritance, data model (Fase 3) | `odoo-module-patterns` |
| Module requirements capture, sprint planning, story points (Fase 1) | `scrum-master` |
| QA, test coverage validation, quality gates (Fase 5) | `odoo-qa` |
| Deploying, reading build logs, Odoo.sh configuration (Fase 6) | `odoo-sh` |
| Production bugs, hotfixes, versioning, post-deploy monitoring (Fase 7) | `odoo-maintenance` |
| Complex Python logic outside Odoo framework | `python-pro` |

## Available Commands (`/slash-command`)

| Command | SDLC Phase | Action |
|---|---|---|
| `/clone-odoo` | 0 - Infraestructura | Clone Odoo Community 19.0 source as local reference. |
| `/sparse-checkout` | 0 — Infraestructura | Filter VS Code workspace to show only relevant modules. |
| `/plan-module` | 1 — Planificación | Capture and validate module requirements before any code. |
| `/explain` | 2 — Análisis | Analyze and explain existing code with full context. |
| `/scaffold-module` | 3 — Diseño | Create a new module (supports OWL & multi-company). |
| `/new-feature` | 3 — Diseño | Design and propose a new feature for an existing module. |
| `/add-field` | 4 — Desarrollo | Add one or more fields to a model (Python + XML + migration). |
| `/add-wizard` | 4 — Desarrollo | Create a transactional wizard (`TransientModel`). |
| `/add-report` | 4 — Desarrollo | Create a QWeb PDF or HTML report. |
| `/fix-issue` | 4 — Desarrollo | Root-cause diagnosis and targeted fix. |
| `/generate-tests` | 5 — Pruebas / QA | Generate `TransactionCase` or `HttpCase` tests. |
| `/perf-check` | 5 — Pruebas / QA | Scan for N+1 queries and ORM optimizations. |
| `/security-audit` | 5 — Pruebas / QA | Audit ACLs, record rules, and `sudo()` usage. |
| `/translate` | 6 — Deploy | Create or update `i18n/es.po` with all missing strings. |
| `/review-pr` | 6 — Deploy | Full quality checklist for Pull Requests. |
| `/changelog` | 6 — Deploy | Generate or update `CHANGELOG.md` with semantic versioning. |
| `/deploy` | 6 — Deploy | Odoo.sh deployment checklist (staging → production). |
| `/hotfix` | 7 — Mantenimiento | Accelerated fix protocol for production-critical bugs. |

## Odoo 19 Conventions (mandatory)

All custom modules must follow these patterns:
- Use `<list>` (not `<tree>`).
- Use direct UI attributes (`invisible="..."`) instead of legacy `attrs="..."`.
- Use `@api.ondelete(at_uninstall=False)` for delete prevention.
- Use `aggregator=` for grouped fields (not `group_operator=`).
- Prefer batch operations (`create([{...}, {...}])`) over loops.
- Avoid N+1: never `search()` inside loops; use batched domains or `read_group()`.
- Use `models.Constraint` instead of `_sql_constraints` for SQL constraints.

## Quality Gates (non-negotiable)

Before marking any task as done:

- **Tests**: Add/adjust `TransactionCase` / `HttpCase` for any behavior change — computed fields, constraints, state transitions, wizard actions, access rules.
- **Security**: ACL and record rules cover all new models. Controllers have the correct `auth` type. No credentials in code.
- **Performance**: No N+1 queries, no expensive loops. Use batching and ORM-friendly patterns.
- **Translations**: All user-facing strings are in `i18n/es.po`.
- **Consistency**: Follow the coding style already present in the repository.

## Module Structure & Naming

- Technical name: `dipl_<module_name>` (always with prefix).
- Version: `19.0.x.y.z`
- License: `LGPL-3`
- Author: `Dipleg`
- Website: `https://dipleg.com`
- XML IDs: namespaced with module prefix, must be stable across versions.
- Security files under `security/` (`ir.model.access.csv` + rules XML when applicable).
- Consider `company_id` and multi-company from the start when relevant.

## Git Flow & Deployment (Odoo.sh)

- **Branches**: `feature/`, `fix/`, `release/`.
- **Commits**: Conventional commits — `feat:`, `fix:`, `docs:`, `test:`, `refactor:`.
- **Staging**: Always test in a staging build before merging to `master`.
- **Production**: Merge only after green build and manual sanity check. Follow `/deploy`.

## Module Versioning

All custom modules use semantic versioning: `19.0.X.Y.Z`.

| Component | When to increment | Example |
|---|---|---|
| Major `X` | Breaking model/API change requiring a migration script | `19.0.2.0.0` |
| Minor `Y` | New backward-compatible feature | `19.0.1.1.0` |
| Patch `Z` | Bug fix, no schema change | `19.0.1.0.1` |

Always update `version` in `__manifest__.py` and add an entry to `CHANGELOG.md` before deploying.

## Translation Standard

- Base msgid/source strings are **English** (the strings written in code).
- Translation output: `i18n/es.po` (Standard Spanish).
- Do NOT generate `i18n/en.po`.

## Debugging Approach

When diagnosing errors:

1. Capture the full error message and stack trace.
2. Identify the most likely trigger path (model method, controller, scheduled action, etc.).
3. Isolate the failure location by searching the codebase (grep on the exception class or message).
4. Implement a minimal fix consistent with the existing coding style and Odoo 19 conventions.
5. Verify the fix via tests or a targeted runtime check.
6. Document: root cause, evidence found, fix applied, test added, prevention recommendation.

**Workflow to use:**
- **Routine bug** (non-urgent, can wait for next release): `/fix-issue`.
- **Production-critical bug** (needs same-day fix): `/hotfix` — accelerated protocol with minimal QA scope.

## Reference Guides

Detailed Odoo 19 API guides: `.agents/skills/odoo-19/references/`
Architectural patterns: `.agents/skills/odoo-module-patterns/references/`
Odoo.sh platform: `.agents/skills/odoo-sh/SKILL.md`
