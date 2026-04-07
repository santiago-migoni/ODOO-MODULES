---
name: odoo-stage-02-functional-definition
description: Functional definition stage workflow for Odoo custom modules. Use when translating discovery findings into a verifiable functional specification with scope, user scenarios, business rules, and acceptance criteria.
---

# Odoo Stage 02 Functional Definition

## Overview
Transform discovery outputs into a complete functional specification that can be validated by business stakeholders and consumed by technical design.
Use `odoo-19` only as a background reference for feasibility context.
Use `business-analyst` to sharpen scenarios, rules, and acceptance criteria, and `product-manager` when scope tradeoffs or prioritization decisions materially affect the spec.

## Required Inputs
- Approved discovery report from stage 01.
- Defined business objectives and process boundaries.
- Stakeholder decisions and unresolved points.
- Regulatory or policy constraints affecting behavior.

## Workflow
1. Convert pain points into functional capabilities.
2. Define user scenarios and expected outcomes by role.
3. Establish explicit in-scope and out-of-scope behavior.
4. Capture business rules, data expectations, and exceptions.
5. Write testable acceptance criteria for each capability.
6. When capability sprawl or release tension appears, use `product-manager` to cut or prioritize scope before handing off to technical design.

## Outputs
- Functional specification with role-based scenarios.
- Scope matrix (in/out) and exception catalog.
- Acceptance criteria set ready for technical mapping.

## Definition of Done
- Every capability has a verifiable acceptance criterion.
- Scope and non-scope are unambiguous for stakeholders.
- Functional behavior is stable enough for technical design.

## Handoff
Provide the stage output to `$odoo-stage-03-technical-design` including:
- Final functional scenarios and business rules.
- Acceptance criteria mapped by capability.
- Open functional questions that may affect architecture.

## Related References
- Use `references/deliverable-template.md` for the main functional specification.
- Use `references/scope-and-acceptance-template.md` when `business-analyst` or `product-manager` is needed to stabilize capability scope, priority, and acceptance criteria.
