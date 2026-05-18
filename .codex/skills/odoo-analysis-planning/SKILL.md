---
name: odoo-analysis-planning
description: Analysis and planning workflow for Odoo custom module delivery. Use when defining the business problem, current state, scope, priorities, risks, success criteria, and the next implementation iteration.
---

# Odoo Analysis Planning

## Overview
Frame the problem before solution design begins.
Use this skill to turn a request into an iteration-ready analysis package with explicit scope, goals, risks, and planning decisions.
Use `odoo-19` only when framework constraints materially affect feasibility.
Use `odoo-project-management` when the work also needs backlog shaping, release slicing, sprint framing, or iterative replanning across multiple increments.

## Required Inputs
- Business objective and target process area.
- Current workflow or pain-point description.
- Stakeholders, roles, and decision owners.
- Constraints such as timeline, budget, compliance, data, or operational limits.
- Known scope requests, assumptions, and open questions.

## Workflow
1. Capture the current state and business problem with enough detail to avoid solution guessing.
2. Identify pain points, root causes, impact, and desired outcomes.
3. Define scope boundaries: in-scope, out-of-scope, and unresolved areas.
4. Translate the request into success criteria, acceptance intent, and priority signals.
5. Identify iteration risks, dependencies, and readiness gaps.
6. Produce the next-iteration plan with explicit assumptions and decision owners.
7. Route to `odoo-design` when the problem statement and scope are stable enough to design the solution.

## Outputs
- Analysis report with current-state diagnosis and pain-point map.
- Scope statement with assumptions, exclusions, and unresolved questions.
- Success criteria and acceptance intent for the next iteration.
- Iteration-ready planning package with priorities, risks, and dependencies.

## Definition of Done
- The business problem and current state are explicit.
- Scope boundaries and success criteria are decision-usable.
- Risks and unknowns are visible enough to begin design.
- The next handoff to design or project coordination is explicit.

## Handoff
- Hand off to `odoo-design` when the solution needs technical definition.
- Hand off to `odoo-project-management` when backlog ordering, sprint framing, release slicing, or replanning must be formalized.
- Hand off back to `odoo-maintenance` or stakeholders when operational evidence is still incomplete and more discovery is required.

## Related References
- Use `references/analysis-deliverable-template.md` for the main analysis output.
- Use `references/discovery-refinement-template.md` when assumptions, pain points, or decisions remain unstable.
- Use `references/scope-and-acceptance-template.md` when the main risk is unclear scope or acceptance intent.
- Use `references/milestone-and-risk-template.md` when the iteration plan needs explicit sequencing or risk control.
