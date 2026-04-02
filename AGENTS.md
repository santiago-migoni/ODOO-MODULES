# Repository Guidelines

## Source of truth

This repository uses Codex as the agent provider.
Primary governance lives in `AGENTS.md` and `.codex/`.

## Repository role in the platform

`ODOO-MODULES` is a companion repository of the `ODOO` dashboard.
The dashboard creates and manages branch-based ephemeral environments for module delivery.

Branch model:
- All branches are ephemeral except `master`.
- `master` is production only.
- Delivery flow is `dev-env -> test-env -> master`.
- A branch can move between dev and test without renaming.
- Demote from test back to dev is allowed when validation fails.
- Merge to `master` is allowed only from test branches via Pull Request.
- There is no fixed naming pattern for non-production branches beyond "not master".

Environment semantics:
- Dev environment: fresh environment without production data, used for full module buildout.
- Test environment: production-like clone with full data from `master`, with production services disabled (for example outbound emails, backups, live messaging).

## Project structure

Installable Odoo 19 modules live at repository root as `dipl_<name>/`.
All custom modules must keep the `dipl_` prefix.

Repository support areas:
- `.codex/`: Codex runtime config, rules, and skills.
- `.codex/agents/`: project-specific subagents for focused implementation and review work.
- `.docs/`: local development documentation and trace records (ignored from VCS).
- `.src/`: local Odoo Community clone for framework and base-module analysis.
- `requirements.txt`: global Python dependency baseline for modules in this repository.

## Operating model

1. Analyze current module state before proposing changes.
2. Implement modules fully in dev branches without touching production.
3. Promote to test branches for production-data validation.
4. Run exhaustive manual audit before production promotion.
5. Merge to `master` only through reviewed PRs from test branches.
6. Keep translations in `i18n/es.po`.

## Quality gates

Manual audit before merge to `master` is mandatory and must verify:
- Traceability of all modified module code.
- Effectiveness of the implemented behavior.
- Efficiency and performance impact.
- Adaptability and maintainability of the solution.

## Skill-first execution

Use `$skill` activation for operational flows.
Skills must be self-contained: no hard dependency on other skills or workflow docs to execute core behavior.

Global technical skill:
- `odoo-19`

Lifecycle skills:
- `odoo-stage-orchestrator`
- `odoo-stage-01-discovery`
- `odoo-stage-02-functional-definition`
- `odoo-stage-03-technical-design`
- `odoo-stage-04-planning`
- `odoo-stage-05-module-scaffolding`
- `odoo-stage-06-implementation`
- `odoo-stage-07-validation-qa`
- `odoo-stage-08-uat`
- `odoo-stage-09-deployment`
- `odoo-stage-10-maintenance`

Governance skill:
- `odoo-dashboard-branch-governance`

Project subagents:
- `code-mapper`
- `frontend-developer`
- `javascript-pro`
- `python-pro`
- `xml-pro`
- `owl-pro`
- `scss-pro`

## Dependencies

Python dependency policy:
- Primary source of truth is `requirements.txt`.
- Any new Python library must be added to `requirements.txt`.
- Add `__manifest__.py -> external_dependencies["python"]` when explicit module-level runtime declaration is required.
