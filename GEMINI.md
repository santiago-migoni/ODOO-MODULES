# Odoo 19 Custom Module Development — Dipleg

Repository constitution for ODOO-MODULES. Governs all custom module development.

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

---

## Iterative SDLC — 8 Phases

Development follows an iterative cycle where each phase produces deliverables that enable the next one. No phases are skipped. Each phase has associated skills and workflows.

### Phase 0: Infrastructure

> **Where we are**: Before writing any code. Setting up the development environment and methodological framework.
> **What to do**: Clone Odoo source, configure sparse-checkout, establish the SDLC framework.
> **How**: Skill `f0-enterprise-sdlc` + workflows `/clone-odoo`, `/sparse-checkout`.
> **Why → enables Phase 1**: Without infrastructure and a methodological framework, planning is based on assumptions. The iterative SDLC establishes the rules of engagement for all subsequent phases.

### Phase 1: Planning & GAP Analysis

> **Where we are**: A business need has been identified. We need to validate it and transform it into an executable backlog.
> **What to do**: Run GAP Analysis (compare need vs standard Odoo), generate a prioritized backlog with logical dependencies, form cross-functional teams (BA, Dev, QA, SPoC), estimate with Fibonacci.
> **How**: Skill `f1-scrum-master` + workflow `/plan-module`.
> **Why → enables Phase 2**: Without a prioritized backlog and resolved dependencies, technical analysis will operate on ambiguous requirements, causing logical blockers and scope creep.

**10/80/10 Rule**: This phase consumes ~10% of the total budget. 80% goes to development/validation. The remaining 10% to support.

### Phase 2: Analysis

> **Where we are**: The backlog is prioritized. Before designing, we map the existing codebase.
> **What to do**: Map modules, models, views, security, computed logic, and impact analysis.
> **How**: Skill `f2-odoo-analysis` + workflow `/explain`.
> **Why → enables Phase 3**: Without analyzing existing code, inheritance and architecture decisions are based on assumptions — leading to refactoring that costs tens of thousands of dollars.

### Phase 3: Architectural Design

> **Where we are**: Analysis has mapped the existing code. We design the module architecture.
> **What to do**: Choose inheritance type (Extension/Classical/Delegation), design data schema, select UI patterns, define directory structure.
> **How**: Skill `f3-module-patterns` + workflows `/scaffold-module`, `/new-feature`.
> **Why → enables Phase 4**: An incorrect inheritance decision has irreversible implications on DB performance. Extension = single table, Classical = new table with copy, Delegation = FK without duplication. The right choice here prevents costly refactoring during implementation.

**Mandatory inheritance decision**: See rule `06-inheritance-strategy`.

### Phase 4: Implementation

> **Where we are**: Architecture is approved. We code following the design.
> **What to do**: Implement in strict order: models → security → views → tests → i18n.
> **How**: Skill `g-odoo-19` (22 specialized references) + workflows `/add-field`, `/add-wizard`, `/add-report`, `/fix-issue`.
> **Why → enables Phase 5**: The order models → security → views prevents the system from attempting to render interfaces on models without defined permissions. Security from the first iteration, not as a patch.

**Mandatory conventions**: See rules `02-odoo-19-conventions`, `07-security-architecture`, `09-owl-frontend`.

### Phase 5: Testing / QA

> **Where we are**: Code is implemented. We validate before deploying.
> **What to do**: Execute the full QA pyramid (5 levels): unit tests → integration → performance → security → smoke test.
> **How**: Skill `f5-odoo-qa` + workflows `/generate-tests`, `/perf-check`, `/security-audit`.
> **Why → enables Phase 6**: Every bug caught in QA costs 10x less than in production (Six Sigma principle). Without rigorous QA, the deploy injects defects directly into corporate operations.

**QA Pyramid**: Unit (TransactionCase) → Integration (HttpCase/Form helper) → Performance (/perf-check) → Security (/security-audit) → Manual smoke test.

### Phase 6: Deploy

> **Where we are**: QA approved. We move code to production through Odoo.sh.
> **What to do**: Validate on staging with production-cloned data, run pre/post migration, deploy, train users.
> **How**: Skill `f6-odoo-sh` + workflows `/translate`, `/review-pr`, `/changelog`, `/deploy`.
> **Why → enables Phase 7**: Without staging with real data, migration scripts could fail against production volumes. A clean deploy minimizes hotfixes and establishes the foundation for the next cycle.

**3-branch strategy**: Dev (demo data, mail catchers) → Staging (production clone, UAT) → Production (explicit merge, transactional update). See rule `08-migration-protocol`.

### Phase 7: Maintenance

> **Where we are**: Module is in production. We manage the post-deploy cycle.
> **What to do**: Diagnose bugs, execute hotfixes, manage versions, monitor post-deploy, close the cycle.
> **How**: Skill `f7-odoo-maintenance` + workflow `/hotfix`.
> **Why → enables Phase 1 (cyclic closure)**: Go-Live is not the end — it's the beginning of the next cycle. Post-deploy findings (UI, integrations, management analytics) feed back into the Phase 1 backlog. Iterative development rejects a rigid endpoint and embraces continuous optimization.

---

## Skill Activation Guide

| Situation | Skill | Phase |
|---|---|---|
| Project kickoff, SDLC framework, GAP Analysis | `f0-enterprise-sdlc` | F0 |
| Sprint planning, story points, backlog | `f1-scrum-master` | F1 |
| Map existing code before designing | `f2-odoo-analysis` | F2 |
| Module structure, inheritance, data model, UI patterns | `f3-module-patterns` | F3 |
| Field types, decorators, ORM methods, views, API, constraints | `g-odoo-19` | Global |
| QA, test coverage, quality gates | `f5-odoo-qa` | F5 |
| Deploy, build logs, Odoo.sh | `f6-odoo-sh` | F6 |
| Production bugs, hotfixes, versioning, post-deploy | `f7-odoo-maintenance` | F7 |

## Available Commands (`/slash-command`)

| Command | Phase | Action |
|---|---|---|
| `/clone-odoo` | F0 | Clone Odoo Community 19.0 source as local reference. |
| `/sparse-checkout` | F0 | Filter VS Code workspace to show only relevant modules. |
| `/plan-module` | F1 | Capture and validate module requirements (includes GAP Analysis). |
| `/explain` | F2 | Analyze and explain existing code with full context. |
| `/scaffold-module` | F3 | Create a new module (supports OWL & multi-company). |
| `/new-feature` | F3 | Design and propose a new feature for an existing module. |
| `/add-field` | F4 | Add one or more fields to a model (Python + XML + migration). |
| `/add-wizard` | F4 | Create a transactional wizard (`TransientModel`). |
| `/add-report` | F4 | Create a QWeb PDF or HTML report. |
| `/fix-issue` | F4 | Root-cause diagnosis and targeted fix. |
| `/generate-tests` | F5 | Generate `TransactionCase` or `HttpCase` tests. |
| `/perf-check` | F5 | Scan for N+1 queries and ORM optimizations. |
| `/security-audit` | F5 | Audit ACLs, record rules, and `sudo()` usage. |
| `/translate` | F6 | Create or update `i18n/es.po` with all missing strings. |
| `/review-pr` | F6 | Full quality checklist for Pull Requests. |
| `/changelog` | F6 | Generate or update `CHANGELOG.md` with semantic versioning. |
| `/deploy` | F6 | Odoo.sh deployment checklist (staging → production). |
| `/hotfix` | F7 | Accelerated fix protocol for production-critical bugs. |

## Odoo 19 Conventions (mandatory)

All custom modules must follow these patterns:

- Use `<list>` (not `<tree>`).
- Use direct UI attributes (`invisible="..."`) instead of legacy `attrs="..."`.
- Use `@api.ondelete(at_uninstall=False)` for delete prevention.
- Use `aggregator=` for grouped fields (not `group_operator=`).
- Prefer batch operations (`create([{...}, {...}])`) over loops.
- Avoid N+1: never `search()` inside loops; use batched domains or `read_group()`.
- Use `models.Constraint` instead of `_sql_constraints` for SQL constraints.
- Declare ALL `@api.depends` paths including deep relational routes. Prefer over-declaring.
- Stored computed fields with editing needs MUST have `inverse`. With filtering needs MUST have `search`.

## Quality Gates (non-negotiable)

Before marking any task as done:

- **Tests**: Add/adjust `TransactionCase` / `HttpCase` for any behavior change. Use `Form` helper for UI-level testing fidelity.
- **Security**: ACL and record rules cover all new models. AND/OR logic validated (see rule `07-security-architecture`). No credentials in code.
- **Performance**: No N+1 queries, no expensive loops. Use batching and ORM-friendly patterns.
- **Translations**: All user-facing strings are in `i18n/es.po`.
- **Consistency**: Follow the coding style already present in the repository and Odoo 19 best practices.

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

Detailed Odoo 19 API guides: `.agents/skills/g-odoo-19/references/`
Architectural patterns: `.agents/skills/f3-module-patterns/references/`
Odoo.sh platform: `.agents/skills/f6-odoo-sh/SKILL.md`
SDLC foundation: `.agents/skills/f0-enterprise-sdlc/SKILL.md`
Full source document: `docs/odoo-enterprise-sdlc.md`
