---
name: odoo-deployment
description: Deployment workflow for Odoo custom module delivery. Use when governing promotion across dev, test, and master contexts, preparing deployment runbooks, freezing release changelogs, defining rollback, and validating post-deploy safety.
---

# Odoo Deployment

## Overview
Govern environment promotion and production release with explicit operational gates.
Use this skill for dev/test/master transition decisions, pre-deploy checks, rollout planning, rollback definition, PR-to-master readiness, and post-deploy verification.
Use `odoo-19` when deployment questions depend on migration-sensitive or framework-specific behavior.
Use `odoo-project-management` when release timing, sequencing, or scope tradeoffs require iteration-level coordination.

## Required Inputs
- Testing package and promotion recommendation from `odoo-testing`.
- Current branch or environment context.
- Release candidate scope, dependency state, and operational constraints.
- Updated module changelog and release notes state.
- Rollback expectations and ownership model.

## Workflow
1. Classify the current release path: stay in dev, promote to test, remain in test, or prepare PR/merge to `master`.
2. Validate readiness gates for the target environment, including implementation completeness, validated scope, changelog state, and manual audit evidence.
3. Freeze `## Unreleased` into a versioned and dated release entry before production recommendation.
4. Build the promotion and deployment runbook with responsibilities, sequencing, and verification checkpoints.
5. Define rollback triggers, rollback path, and post-deploy validation.
6. Produce the release recommendation with explicit pass/fail blockers.

## Outputs
- Environment-promotion decision and gating report.
- Deployment runbook with pre-deploy, deploy, and post-deploy checks.
- Rollback procedure with trigger conditions.
- Release-ready changelog status for each affected module.

## Definition of Done
- Promotion path and release gates are explicit.
- Rollback is operationally feasible.
- Production recommendation is tied to validated evidence, not assumptions.
- The branch and environment decision is unambiguous.

## Handoff
- Hand off to `odoo-maintenance` after deployment preparation or production release, including support baseline and monitoring checkpoints.
- Hand off to `odoo-project-management` when release timing, scope, or promotion readiness must be re-planned.
- Hand off back to `odoo-testing` or `odoo-coding` when release blockers invalidate promotion.

## Related References
- Use `references/deployment-deliverable-template.md` for the deployment handoff structure.
- Use `references/module-changelog-template.md` as the release changelog format.
- Use `references/module-changelog-policy.md` for changelog gates.
- Use `references/manual-audit-checklist.md` for production-readiness review.
