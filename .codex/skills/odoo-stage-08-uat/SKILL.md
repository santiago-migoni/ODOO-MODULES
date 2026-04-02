---
name: odoo-stage-08-uat
description: User acceptance testing stage workflow for Odoo custom modules. Use when coordinating business-user validation, capturing structured feedback, and deciding acceptance versus required adjustments.
---

# Odoo Stage 08 UAT

## Overview
Coordinate user acceptance testing with role-specific scripts, structured feedback capture, and explicit acceptance decisions.
Use `odoo-19` references only when UAT findings require technical clarification.

## Required Inputs
- QA approval package from stage 07.
- Business-user participant list and role mapping.
- UAT scenarios aligned with acceptance criteria.
- Decision model for acceptance, conditional acceptance, or rejection.

## Workflow
1. Prepare role-based UAT scripts and evidence capture templates.
2. Run UAT sessions with structured observation and logging.
3. Classify feedback into defects, enhancements, or training gaps.
4. Evaluate acceptance criteria status with business owners.
5. Record final acceptance decision and required actions.

## Outputs
- UAT execution script by role and scenario.
- Feedback report with categorized findings and priorities.
- Business acceptance record with closure conditions.

## Definition of Done
- UAT findings are complete, categorized, and owner-assigned.
- Acceptance decision is explicit and evidence-backed.
- Required adjustments are either closed or formally planned.

## Handoff
Provide the stage output to `$odoo-stage-09-deployment` including:
- Final acceptance status and approved scope.
- Mandatory fixes or approved deferrals.
- Deployment preconditions accepted by business stakeholders.
