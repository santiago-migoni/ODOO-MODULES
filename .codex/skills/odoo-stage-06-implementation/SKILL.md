---
name: odoo-stage-06-implementation
description: Implementation stage workflow for Odoo custom modules. Use when executing iterative coding slices across backend, views, security, data files, tests, and translations under an approved technical design.
---

# Odoo Stage 06 Implementation

## Overview
Execute coding slices in a controlled sequence that preserves traceability to functional criteria and technical design decisions.
Use `odoo-19` as the primary technical reference during development.
Use `odoo-project-management` when implementation needs sprint backlog control, daily coordination, flow visualization, blocker escalation, or increment framing.

## Required Inputs
- Approved scaffolding and planning package from stages 04-05.
- Technical design decisions from stage 03.
- Functional acceptance criteria from stage 02.
- Slice-level priorities and dependency order.

## Workflow
1. Implement one slice at a time with clear scope boundaries.
2. Apply backend, view, security, data, test, and i18n changes coherently.
3. Keep traceability from code changes to acceptance criteria.
4. Update the affected module `CHANGELOG.md` under `## Unreleased` whenever a slice introduces relevant functional, technical, compatibility, hardening, or testing impact.
5. Validate each slice before moving to the next one.
6. Record deviations, tradeoffs, follow-up items, and changelog exceptions when relevant.

## Outputs
- Slice-by-slice implementation plan and execution log.
- Traceability map from code changes to acceptance criteria.
- Implementation notes for QA and UAT preparation.
- Changelog status for each affected module before QA handoff.

## Definition of Done
- Each planned slice is implemented and validated.
- No accepted slice lacks test or translation consideration.
- No completed slice omits required changelog consideration for the affected module.
- Technical and functional traceability is preserved.

## Handoff
Provide the stage output to `$odoo-stage-07-validation-qa` including:
- Completed slice list and change summary.
- Test targets and known risk areas.
- Evidence links for acceptance-criterion coverage.
- Current `CHANGELOG.md` status for the affected modules.

## Related References
- Use `references/deliverable-template.md` for the implementation handoff structure.
- Use `../odoo-dashboard-branch-governance/references/module-changelog-policy.md` for module changelog gate rules.
- Use `../odoo-project-management/references/sprint-management-template.md` when implementation work is being managed as a sprint with daily synchronization, blocker tracking, and increment reporting.
