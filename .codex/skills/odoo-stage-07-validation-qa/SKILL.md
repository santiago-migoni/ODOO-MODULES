---
name: odoo-stage-07-validation-qa
description: Validation and QA stage workflow for Odoo custom modules. Use when evaluating implemented slices through technical, functional, and regression testing with explicit release-approval criteria.
---

# Odoo Stage 07 Validation QA

## Overview
Build and execute a validation strategy that verifies functional behavior, technical quality, and regression safety before user acceptance testing.
Use `odoo-19` testing and security references when defining coverage and risk depth.

## Required Inputs
- Implementation outputs and evidence from stage 06.
- Functional acceptance criteria from stage 02.
- Technical constraints and risk map from stages 03-04.
- Test environment readiness and data scenarios.

## Workflow
1. Build a QA matrix covering functional, technical, and regression dimensions.
2. Prioritize tests by business criticality and risk exposure.
3. Define severity model and release-blocking conditions.
4. Execute or plan targeted tests with evidence requirements.
5. Produce go/no-go recommendation for UAT.

## Outputs
- QA matrix with test scope, ownership, and priority.
- Defect severity model with blocking thresholds.
- Validation summary and UAT entry recommendation.

## Definition of Done
- Coverage minimum is defined and evidence-backed.
- Blocking severity conditions are explicit.
- UAT entry criteria are met or clearly blocked.

## Handoff
Provide the stage output to `$odoo-stage-08-uat` including:
- QA-approved scope and known limitations.
- Outstanding defects and risk acceptance decisions.
- User-facing test scenarios ready for business validation.
