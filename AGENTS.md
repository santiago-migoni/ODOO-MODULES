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
Use only subcommands currently available in `rtk --help`; do not assume aliases or unsupported verbs.
Prefer the token-optimized wrappers listed by `rtk --help` over raw shell commands whenever they cover the same task.

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

Reference examples:
- `19.0.1.0.0` = first stable release of a functional line.
- `19.0.1.1.0` = small/medium functional improvement without changing the release line.
- `19.0.1.1.1` = corrective bugfix/hardening patch.
- `19.0.2.0.0` = important new functional capability (new functional line).
- `19.0.3.0.0` = larger functional scope jump (next functional line).
- `20.0.1.0.0` = migration to Odoo 20.

Version decision protocol (mandatory for Codex):
- Before finalizing module changes, classify the change as `x`, `y`, or `z` impact and apply the corresponding bump in `__manifest__.py`.
- Keep `CHANGELOG.md` and `__manifest__.py` aligned on the same released version.
- In the final implementation report, state explicitly which bump type was applied (`x`, `y`, or `z`) and why.
- If no functional/technical module change occurred, do not bump version.

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

## Iterative delivery policy

The delivery process is cyclical and iteration-based, not a rigid linear pipeline.

Canonical lifecycle:
1. Analysis and planning
2. Design
3. Development
4. Testing
5. Deployment
6. Maintenance

Operational rules:
- Treat the lifecycle as an iterative loop, not a one-way sequence.
- Any stage may return work to a previous stage when new evidence, defects, deployment blockers, benchmarking results, or production learning invalidate the current path.
- For every user request, identify the dominant current stage before acting.
- Deliver the artifact that belongs to the current stage instead of prematurely jumping to later-stage work.
- When a stage changes, make the transition explicit and state what evidence or decision enabled it.

Stage dominance guidance:
- Use Analysis and planning when the problem, scope, priorities, or existing-solution landscape are still unclear.
- Use Design when the problem is clear but the module structure, contracts, dependencies, or technical approach are not yet fixed.
- Use Development only after the target slice is sufficiently designed.
- Use Testing when the slice already exists and needs technical or functional validation.
- Use Deployment when the validated slice is ready for environment promotion.
- Use Maintenance when the slice is already in use and the work is incident response, hardening, adaptation, or post-release correction.

## Benchmark and reuse policy

Analysis and planning must include existing-solution discovery when the request touches standard business flows, localizations, or patterns already common in Odoo ecosystems.

Discovery sources, in order:
1. Odoo standard behavior and source modules
2. Local `.src/` framework and addon references
3. Trusted partner ecosystems and benchmark repositories
4. Existing Dipleg modules already present in this repository

Benchmark scope must answer:
- Does Odoo already solve this?
- Does a trusted partner already solve this?
- Is the solution functional, technical, documental, or mixed?
- Is the candidate suitable for adopt, extend, inspire, or discard?

Decision policy for external solutions:
- Adopt: when the existing solution fits the requirement with acceptable dependencies and ownership tradeoffs.
- Extend: when the existing solution solves most of the problem but needs Dipleg-specific policy, layout, or integration.
- Inspire: when the solution provides a useful pattern but should not become a production dependency.
- Discard: when the solution creates excessive coupling, solves a different problem, or conflicts with Dipleg architecture.

Ownership rule:
- External modules and partner repositories are sources of learning, reuse, or extension.
- Dipleg-owned production behavior must remain understandable, governable, and traceable from this repository.
- Do not adopt external code blindly. Always evaluate architectural fit, dependency cost, upgrade risk, and document ownership impact.

## Stage outputs policy

Expected outputs by stage:
- Analysis and planning: problem framing, benchmark, gap analysis, priorities, risks, success criteria.
- Design: architecture, module boundaries, dependencies, contracts, data/report/view strategy.
- Development: coherent implementation slice with versioning, changelog, and README alignment.
- Testing: technical and functional validation evidence, failures, regressions, and release readiness.
- Deployment: promotion plan, rollout execution, rollback posture, and post-deploy verification.
- Maintenance: incident diagnosis, corrective change, hardening decision, and recycled backlog input for the next iteration.

Execution rule:
- If the user asks for code, do not stop at abstract planning unless the current stage is genuinely unresolved.
- If the current stage is unresolved, do not force implementation; first close the missing analysis or design decision.

Global technical skill:
- `odoo-19`

Transversal delivery skill:
- `odoo-project-management`

Lifecycle skills:
- `odoo-analysis-planning`
- `odoo-design`
- `odoo-coding`
- `odoo-testing`
- `odoo-deployment`
- `odoo-maintenance`

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

Business and coordination subagents (`business-analyst`, `product-manager`, `project-manager`) are transversal support roles for ambiguity reduction, prioritization, sequencing, and readiness decisions.
They do not replace the six operational lifecycle skills.

`odoo-project-management` is the transversal coordination skill for Agile, Lean, Kanban, and Scrum execution.
It governs backlog, sprint cadence, adaptation, release coordination, and iterative closure across the six operational stages, but it does not absorb their execution responsibilities.

## Dependencies

Python dependency policy:
- Primary source of truth is `requirements.txt`.
- Any new Python library must be added to `requirements.txt`.
- Add `__manifest__.py -> external_dependencies["python"]` when explicit module-level runtime declaration is required.
