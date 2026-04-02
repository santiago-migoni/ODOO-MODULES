---
name: odoo-stage-10-maintenance
description: Maintenance stage workflow for Odoo custom modules. Use when running post-release operations including incident triage, hotfix prioritization, SLA-driven response, and iterative enhancement planning.
---

# Odoo Stage 10 Maintenance

## Overview
Operate a structured post-release maintenance cycle covering incident management, hotfix execution, service-level response, and planned improvements.
Use `odoo-19` references when diagnosing framework-level root causes or designing safe fixes.

## Required Inputs
- Deployment baseline and known issues from stage 09.
- Incident intake channels and escalation policy.
- Service-level expectations and business criticality map.
- Capacity model for hotfixes and enhancements.

## Workflow
1. Classify incoming issues by impact, urgency, and scope.
2. Apply SLA-driven triage and ownership assignment.
3. Define hotfix versus planned enhancement path.
4. Track resolution evidence and regression safeguards.
5. Feed lessons learned back into the next development cycle.

## Outputs
- Incident classification and SLA response protocol.
- Hotfix and enhancement decision log.
- Maintenance backlog with cycle feedback inputs.

## Definition of Done
- Incident and hotfix workflow is operational and measurable.
- SLA commitments and escalation rules are explicit.
- Maintenance outputs are ready to seed new discovery/planning cycles.

## Handoff
Provide the stage output back to `$odoo-stage-01-discovery` for the next cycle including:
- Production learnings and recurring pain patterns.
- Prioritized improvement opportunities.
- Confirmed constraints discovered in operations.
