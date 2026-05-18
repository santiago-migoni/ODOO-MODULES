---
name: odoo-maintenance
description: Maintenance workflow for Odoo custom module delivery. Use when handling post-release incidents, hotfixes, operational learning, backlog recycling, and continuous improvement after deployment.
---

# Odoo Maintenance

## Overview
Run the post-release operating loop.
Use this skill to manage incidents, hotfix decisions, operational risk, recurring issues, and the recycling of production learning into the next iteration.
Use `odoo-19` when diagnosing framework-level root causes or designing safe fixes.
Use `odoo-project-management` when maintenance findings must be turned into backlog updates, retrospectives, or project closeout decisions.

## Required Inputs
- Deployment baseline and release scope from `odoo-deployment`.
- Incident reports, support signals, and operational constraints.
- Severity expectations, service commitments, and ownership model.
- Known deferred issues, accepted risks, and improvement opportunities.

## Workflow
1. Classify incidents and maintenance requests by impact, urgency, and scope.
2. Decide hotfix versus planned-iteration treatment.
3. Define resolution path, safeguards, and regression expectations.
4. Track recurring issues, debt patterns, and operational constraints discovered in production.
5. Feed reusable learning back into analysis, planning, and project coordination.

## Outputs
- Incident and maintenance decision log.
- Hotfix versus enhancement routing decision.
- Maintenance backlog and operational learning package.
- Inputs for the next analysis/planning cycle.

## Definition of Done
- Incident handling and enhancement routing are explicit.
- Operational learning is preserved instead of remaining implicit.
- The next cycle receives reusable constraints, risks, and opportunities.
- Ownership and escalation expectations are clear.

## Handoff
- Hand off to `odoo-analysis-planning` when production learning should seed the next iteration.
- Hand off to `odoo-project-management` when maintenance outcomes require backlog updates, retrospectives, or closure artifacts.
- Hand off to `odoo-coding` only when an approved hotfix path is already defined.

## Related References
- Use `references/maintenance-deliverable-template.md` for the maintenance handoff structure.
- Use `../odoo-project-management/references/review-retrospective-template.md` when incidents should feed iterative improvement actions.
- Use `../odoo-project-management/references/project-closeout-template.md` when a release cycle or project should be formally closed.
