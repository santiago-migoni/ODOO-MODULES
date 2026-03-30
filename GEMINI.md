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
| Planning module structure, inheritance, data model | `odoo-module-patterns` |
| Deploying, reading build logs, Odoo.sh configuration | `odoo-sh` |
| Complex Python logic outside Odoo framework | `python-pro` |
| Sprint planning, story points, backlog management | `scrum-master` |

## Available Commands (`/slash-command`)

| Command | Action |
|---|---|
| `/scaffold-module` | Create a new module (supports OWL & multi-company). |
| `/new-feature` | Add new functionality to an existing module. |
| `/add-field` | Add one or more fields to a model (Python + XML + migration). |
| `/add-wizard` | Create a transactional wizard (`TransientModel`). |
| `/add-report` | Create a QWeb PDF or HTML report. |
| `/generate-tests` | Generate `TransactionCase` or `HttpCase` tests. |
| `/translate` | Create or update `i18n/es.po` with all missing strings. |
| `/security-audit` | Audit ACLs, record rules, and `sudo()` usage. |
| `/perf-check` | Scan for N+1 queries and ORM optimizations. |
| `/deploy` | Odoo.sh deployment checklist (staging → production). |
| `/fix-issue` | Root-cause diagnosis and fix. |
| `/review-pr` | Full quality checklist for Pull Requests. |

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

## Reference Guides

Detailed Odoo 19 API guides: `.agents/skills/odoo-19/references/`
Architectural patterns: `.agents/skills/odoo-module-patterns/references/`
Odoo.sh platform: `.agents/skills/odoo-sh/SKILL.md`
