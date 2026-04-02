---
name: odoo-stage-09-deployment
description: Deployment stage workflow for Odoo custom modules on Odoo.sh. Use when preparing release runbooks, pre/post-deploy checks, rollback plans, and production promotion from development through testing.
---

# Odoo Stage 09 Deployment

## Overview
Create and validate a deployment runbook for Odoo.sh promotion flow (`desarrollo -> prueba -> produccion`), including rollback and post-release verification.
Use `odoo-19` references for migration-sensitive or framework-specific deployment concerns.

## Required Inputs
- Accepted UAT package from stage 08.
- Release candidate scope and dependency state.
- Environment promotion path and release windows.
- Operational readiness and rollback constraints.

## Workflow
1. Define pre-deploy checks and release prerequisites.
2. Plan promotion sequence across Odoo.sh environments.
3. Define rollback strategy and activation criteria.
4. Build post-deploy verification checklist by critical flow.
5. Produce deployment communication and responsibility matrix.

## Outputs
- End-to-end deployment runbook for Odoo.sh.
- Pre-deploy and post-deploy checklists.
- Rollback procedure with trigger conditions.

## Definition of Done
- Deployment sequence is explicit and rehearsable.
- Rollback path is defined and operationally feasible.
- Production verification criteria are complete.

## Handoff
Provide the stage output to `$odoo-stage-10-maintenance` including:
- Production baseline and deployed scope.
- Known deferred issues and risk notes.
- Monitoring checkpoints and support ownership.
