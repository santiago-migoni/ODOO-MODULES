---
name: odoo-project-management
description: Transversal project management workflow for Odoo custom module delivery. Use when governing iterative delivery through vision framing, backlog management, sprint cadence, adaptation, release coordination, and project closure across the six operational stages.
---

# Odoo Project Management

## Overview
Coordinate the iterative delivery system without replacing the operational stage skills.
Use this skill when the work needs cross-cutting management: product vision, backlog ordering, sprint framing, blocker handling, adaptation, release coordination, branch-promotion decisions, or structured closeout.

This skill is transversal.
It coordinates `odoo-analysis-planning`, `odoo-design`, `odoo-coding`, `odoo-testing`, `odoo-deployment`, and `odoo-maintenance`, but it does not replace them.

## Required Inputs
- Current project or module objective.
- Current stage or iteration state.
- Known scope, constraints, stakeholders, and success criteria.
- Existing backlog, sprint status, blockers, or feedback when available.
- Target horizon: next iteration, release slice, promotion decision, or project closeout.

## Operating Modes
Use one mode explicitly:

### `visualize`
- Define the project frame: vision, scope boundaries, stakeholders, constraints, and working model.

### `speculate`
- Shape or refresh backlog, release slices, priorities, dependencies, and delivery hypotheses.

### `explore`
- Manage active iteration flow: sprint goal, sprint backlog, blockers, WIP pressure, and increment focus.

### `adapt`
- Replan from evidence after testing, stakeholder feedback, incidents, or release friction.

### `close`
- Produce structured closure: residual risks, unresolved debt, outcomes, and reusable learning.

## Workflow
1. Identify whether the current need is framing, backlog shaping, active iteration control, adaptation, release coordination, or closure.
2. Select the matching mode and relevant reference template.
3. Make the current iteration state explicit across the six operational stages.
4. Convert findings into a concrete coordination artifact: backlog, sprint frame, release decision, adaptation package, or closeout.
5. Route the next action to the right operational skill instead of absorbing execution into project management.

## Outputs
- Vision and working-model package.
- Prioritized backlog and release-slice plan.
- Sprint coordination package with blockers and next increment focus.
- Adaptation package based on testing, deployment, or maintenance evidence.
- Release-coordination or closeout artifact with explicit next steps.

## Definition of Done
- The selected project-management mode matches the actual delivery need.
- Coordination decisions are concrete enough to guide the next action.
- Iterative flow, release gates, and feedback loops are explicit.
- The next handoff to an operational skill is unambiguous.

## Handoff
- Hand off to `odoo-analysis-planning` when the main need is problem framing or iteration planning.
- Hand off to `odoo-design` when solution tradeoffs are ready for technical definition.
- Hand off to `odoo-coding` when sprint execution or slice implementation should begin or continue.
- Hand off to `odoo-testing` when validation findings and readiness decisions need formal consolidation.
- Hand off to `odoo-deployment` when promotion, release timing, or branch-governance decisions must be executed.
- Hand off to `odoo-maintenance` when post-release incidents, learnings, or service-level issues become the main driver.

## Related References
- Use `references/vision-and-working-model-template.md` for `visualize`.
- Use `references/backlog-and-release-template.md` for `speculate`.
- Use `references/sprint-management-template.md` for `explore`.
- Use `references/review-retrospective-template.md` for `adapt`.
- Use `references/project-closeout-template.md` for `close`.
