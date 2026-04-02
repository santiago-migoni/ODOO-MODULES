---
name: odoo-stage-06-implementation
description: Implementation stage workflow for Odoo custom modules. Use when executing iterative coding slices across backend, views, security, data files, tests, and translations under an approved technical design.
---

# Odoo Stage 06 Implementation

## Overview
Execute coding slices in a controlled sequence that preserves traceability to functional criteria and technical design decisions.
Use `odoo-19` as the primary technical reference during development.

## Required Inputs
- Approved scaffolding and planning package from stages 04-05.
- Technical design decisions from stage 03.
- Functional acceptance criteria from stage 02.
- Slice-level priorities and dependency order.

## Workflow
1. Implement one slice at a time with clear scope boundaries.
2. Apply backend, view, security, data, test, and i18n changes coherently.
3. Keep traceability from code changes to acceptance criteria.
4. Validate each slice before moving to the next one.
5. Record deviations, tradeoffs, and follow-up items.

## Outputs
- Slice-by-slice implementation plan and execution log.
- Traceability map from code changes to acceptance criteria.
- Implementation notes for QA and UAT preparation.

## Definition of Done
- Each planned slice is implemented and validated.
- No accepted slice lacks test or translation consideration.
- Technical and functional traceability is preserved.

## Handoff
Provide the stage output to `$odoo-stage-07-validation-qa` including:
- Completed slice list and change summary.
- Test targets and known risk areas.
- Evidence links for acceptance-criterion coverage.
