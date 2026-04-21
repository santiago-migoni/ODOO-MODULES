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

## Terminal tooling

Use `rtk` as the preferred terminal proxy for read-heavy inspection and compact command output when it improves signal quality.

Preferred `rtk` commands:
- `rtk read` for file reading.
- `rtk find` and `rtk tree` for repository exploration.
- `rtk diff` for compact change review.
- `rtk grep` for filtered text search output.
- `rtk git` for read-only Git inspection when concise output is useful.
- `rtk test`, `rtk err`, and `rtk summary` for compact validation and failure-focused output.

Usage boundaries:
- Do not use `rtk` to bypass repository safety, branch governance, or dependency rules.
- Treat `rtk git` as read-only by default unless the user explicitly requests a Git mutation.
- Treat `rtk trust`, `rtk untrust`, `rtk proxy`, and `rtk config` as governance-sensitive commands.
- If `rtk gain` fails because its tracking database is unavailable, continue with normal `rtk` subcommands instead of blocking work.

## Operating model

1. Analyze current module state before proposing changes.
2. Implement modules fully in dev branches without touching production.
3. Promote to test branches for production-data validation.
4. Run exhaustive manual audit before production promotion.
5. Merge to `master` only through reviewed PRs from test branches.
6. Keep translations in `i18n/<locale>.po`; use `i18n/es.po` as the default Spanish fallback, and use regional files such as `i18n/es_AR.po` when the operating language requires locale-specific translations.

## Quality gates

Manual audit before merge to `master` is mandatory and must verify:
- Traceability of all modified module code.
- Effectiveness of the implemented behavior.
- Efficiency and performance impact.
- Adaptability and maintainability of the solution.

## Changelog Policy

Every installable `dipl_*` module must include `CHANGELOG.md` at the module root.
Changelog ownership is per module, not global to the repository.

Relevant changes that must be reflected in `CHANGELOG.md` include:
- Functional behavior changes.
- Technical architecture or hardening changes.
- Compatibility changes across Odoo modules or environments.
- Relevant testing additions, fixes, or release-safety improvements.

Operational rules:
- During development, record relevant changes under `## Unreleased`.
- Before promoting a branch to test, `CHANGELOG.md` must be updated for the module scope under review.
- Before opening a PR to `master`, `## Unreleased` must be frozen into a versioned and dated release entry.
- Missing or outdated changelog entries block promotion to test and production recommendation.

Repository support notes:
- `.docs/` may complement delivery traceability, but it does not replace `CHANGELOG.md`.
- Changelog content must be manual and curated; do not generate it mechanically from commits.

## Manifest Version Policy

For Dipleg installable modules, `__manifest__.py["version"]` must use the format `19.0.x.y.z`.

Semantic meaning:
- `x` = version
- `y` = improvement
- `z` = corrections

Operational rules:
- Increment `x` for a new functional release line or scope version that materially changes the delivered module contract.
- Increment `y` for additive or release-level improvements that remain within the same functional release line.
- Increment `z` for corrective fixes, hardening, or patch-level adjustments within the same release/improvement line.
- Keep the Odoo major prefix aligned with the target framework version (`19.0` for Odoo 19).

## README Policy

Every installable `dipl_*` module must include `README.md` at the module root.
README ownership is per module, not global to the repository.

Minimum README content must cover:
- Module purpose and business intent.
- Current functional policy and operating model.
- Main dependencies and configuration assumptions.
- Main user-visible flows, fields, or integration contracts.
- Known limitations, validation notes, or operational caveats when relevant.

Operational rules:
- When scaffolding a new module, create `README.md` as part of the baseline module structure.
- When a module changes in ways that affect functionality, operator workflow, pricing logic, integration behavior, or current implementation policy, update `README.md`.
- Before promoting a branch to test, `README.md` must match the validated module scope and current behavior.
- Missing or outdated module README content blocks promotion recommendation to test and production.

Repository support notes:
- `.docs/` may complement implementation or QA detail, but it does not replace the module `README.md`.
- `README.md` should describe the module as it currently behaves, not as it behaved in previous intermediate iterations.

## Skill-first execution

Use `$skill` activation for operational flows.
Skills must be self-contained: no hard dependency on other skills or workflow docs to execute core behavior.

Global technical skill:
- `odoo-19`

Transversal delivery skill:
- `odoo-project-management`

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
- `business-analyst`
- `code-mapper`
- `frontend-developer`
- `javascript-pro`
- `product-manager`
- `project-manager`
- `python-pro`
- `xml-pro`
- `owl-pro`
- `scss-pro`

Business and coordination subagents (`business-analyst`, `product-manager`, `project-manager`) are transversal support roles for early lifecycle stages and governance decisions.
They do not replace lifecycle skills; they help produce clearer artifacts, priorities, and readiness decisions inside the stage flow.

`odoo-project-management` is the transversal delivery governance skill for Agile, Lean, Kanban, and Scrum execution.
It does not replace lifecycle stages or the `project-manager` subagent; it coordinates backlog, sprint cadence, adaptation, and closure across them.

## Dependencies

Python dependency policy:
- Primary source of truth is `requirements.txt`.
- Any new Python library must be added to `requirements.txt`.
- Add `__manifest__.py -> external_dependencies["python"]` when explicit module-level runtime declaration is required.
