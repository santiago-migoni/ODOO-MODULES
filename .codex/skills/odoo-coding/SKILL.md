---
name: odoo-coding
description: Coding workflow for Odoo custom module delivery. Use when implementing approved slices across backend, views, security, data files, reports, tests, and translations with explicit traceability to the agreed design.
---

# Odoo Coding

## Overview
Execute one implementation slice at a time under a defined design and with explicit traceability to business intent.
Use `odoo-19` as the primary technical reference during development.
Use `odoo-project-management` when coding must be framed as sprint execution, blocker handling, or increment reporting across multiple slices.

## Required Inputs
- Approved design package from `odoo-design`.
- Scope and success criteria from `odoo-analysis-planning`.
- Slice priorities and dependency order.
- Current module state and any release-safety constraints.

## Workflow
1. Implement one slice at a time with clear scope boundaries.
2. Apply backend, XML, security, data, report, test, and i18n changes coherently.
3. Preserve traceability from code changes to design decisions and acceptance intent.
4. Update the affected module `CHANGELOG.md` under `## Unreleased` whenever the slice introduces relevant functional, technical, compatibility, hardening, or testing impact.
5. Update the affected module `README.md` whenever the slice changes current functionality, operator workflow, integration behavior, or declared module policy.
6. Validate the slice enough to support QA handoff.
7. Record deviations, tradeoffs, and follow-up work before moving to the next slice.

## Outputs
- Slice implementation package with traceability to design and scope.
- Execution notes for testing and release preparation.
- Current changelog and README status for each affected module.
- Follow-up list for deferred issues, tradeoffs, and open risks.

## Definition of Done
- Each implemented slice is traceable to the approved design and scope.
- Required changelog and README updates are considered for every affected module.
- Testing handoff is possible without reconstructing implementation intent.
- Deviations and residual risks are explicit.

## Handoff
- Hand off to `odoo-testing` when the implemented scope is ready for technical and functional validation.
- Hand off to `odoo-project-management` when blocker escalation, replanning, or slice reprioritization is needed.
- Hand off back to `odoo-design` when implementation exposes unresolved architectural flaws or invalid technical assumptions.

## Related References
- Use `references/coding-deliverable-template.md` for the implementation handoff structure.
- Use `references/module-changelog-policy.md` for changelog gate rules during development.
