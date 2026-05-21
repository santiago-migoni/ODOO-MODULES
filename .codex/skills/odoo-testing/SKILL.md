---
name: odoo-testing
description: Testing workflow for Odoo custom module delivery. Use when validating implemented scope through technical, regression, QA, and business-facing acceptance readiness checks before environment promotion.
---

# Odoo Testing

## Overview
Validate the implemented increment before promotion decisions are made.
Use this skill to combine technical validation, functional QA, regression coverage, and acceptance-readiness framing in one evidence package.
Use `odoo-19` testing and security references when defining coverage depth or investigating framework-level risks.
Use `odoo-project-management` when findings must trigger backlog adaptation, sprint review decisions, or scope replanning.

## Required Inputs
- Implemented scope and evidence from `odoo-coding`.
- Scope and success criteria from `odoo-analysis-planning`.
- Design risks and constraints from `odoo-design`.
- Target environment, data scenarios, and promotion expectations.

## Workflow
1. Build a validation matrix covering technical, functional, regression, and user-facing scenarios.
2. Prioritize tests by business criticality, defect cost, and release risk.
3. Define severity thresholds, blocking conditions, and acceptance-readiness criteria.
4. Verify that `CHANGELOG.md` and `README.md` reflect the validated scope.
5. Execute or plan targeted tests with explicit evidence expectations.
6. Consolidate findings, residual risks, and release recommendations.
7. Route to `odoo-deployment` only when promotion readiness is explicit.

## Outputs
- Validation matrix with scope, priority, ownership, and evidence expectations.
- Defect and risk summary with blocking thresholds.
- Acceptance-readiness package for promotion decisions.
- Changelog and README consistency status for affected modules.

## Definition of Done
- Technical and functional coverage expectations are explicit.
- Blocking conditions and accepted risks are documented.
- The validated scope matches changelog and README claims, or mismatches are explicit.
- Promotion readiness or rework direction is unambiguous.

## Handoff
- Hand off to `odoo-deployment` when the increment is ready for environment promotion and release governance.
- Hand off to `odoo-project-management` when testing findings must feed backlog reprioritization or iteration adaptation.
- Hand off back to `odoo-coding` when fixes are required before promotion.

## Related References
- Use `references/testing-deliverable-template.md` for the validation handoff structure.
- Use `references/manual-audit-checklist.md` for production-readiness review gates.
- Use `references/module-changelog-policy.md` for changelog consistency checks.
