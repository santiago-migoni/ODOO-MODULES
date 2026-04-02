---
name: odoo-stage-04-planning
description: Planning stage workflow for Odoo custom modules. Use when converting technical design into an executable iteration plan with milestones, dependencies, risk controls, and delivery sequencing.
---

# Odoo Stage 04 Planning

## Overview
Convert technical design into a delivery plan with iteration slices, priorities, risks, dependencies, and explicit acceptance gates.
Use `odoo-19` references only when planning depends on framework-specific implementation constraints.

## Required Inputs
- Approved technical design from stage 03.
- Team capacity and timeline constraints.
- Dependency and environment readiness status.
- Target release window and risk tolerance.

## Workflow
1. Break scope into implementation slices with clear outcomes.
2. Sequence slices by dependency and business value.
3. Estimate effort and identify capacity bottlenecks.
4. Define risk mitigation actions and escalation triggers.
5. Set iteration gates and review checkpoints.

## Outputs
- Iteration plan with prioritized backlog and milestones.
- Dependency and risk register with owners.
- Delivery gates and acceptance checkpoint schedule.

## Definition of Done
- Backlog is sequenced, prioritized, and estimable.
- Risks have owners and mitigation actions.
- Iteration gates are clear for execution kickoff.

## Handoff
Provide the stage output to `$odoo-stage-05-module-scaffolding` including:
- First implementation slice scope.
- Module/package boundaries for scaffolding.
- Planning assumptions that affect code structure.
