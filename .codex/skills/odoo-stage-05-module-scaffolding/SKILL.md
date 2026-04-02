---
name: odoo-stage-05-module-scaffolding
description: Module scaffolding stage workflow for Odoo custom modules. Use when initializing module structure and baseline artifacts so implementation can proceed on a coherent Odoo 19 foundation.
---

# Odoo Stage 05 Module Scaffolding

## Overview
Define and verify the minimum Odoo 19 module skeleton required to start implementation with structural consistency and deployment readiness.
Use `odoo-19` references for manifest, data loading, and view structure conventions.

## Required Inputs
- Approved first-slice plan from stage 04.
- Module naming and dependency decisions.
- Baseline security and data loading expectations.
- Repository conventions (prefix, i18n, tests, manifests).

## Workflow
1. Define the target module inventory and ownership boundaries.
2. Confirm required baseline files and folders per module.
3. Define manifest baseline with dependencies and data hooks.
4. Confirm initial security, views, and i18n placeholders.
5. Validate scaffolding checklist against Odoo 19 conventions.

## Outputs
- Scaffolding checklist and expected module file map.
- Baseline manifest and dependency definition standard.
- Initialization readiness report for implementation.

## Definition of Done
- Minimum module structure is complete and coherent.
- Manifest baseline is consistent with planned dependencies.
- Scaffolding is ready for incremental implementation slices.

## Handoff
Provide the stage output to `$odoo-stage-06-implementation` including:
- Confirmed module skeleton and boundaries.
- Baseline manifests and loading order assumptions.
- Initial technical constraints to enforce during coding.
