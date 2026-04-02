---
name: odoo-stage-03-technical-design
description: Technical design stage workflow for Odoo custom modules. Use when turning an approved functional specification into a concrete technical design for models, views, security, data files, automation, and integration boundaries.
---

# Odoo Stage 03 Technical Design

## Overview
Create a decision-complete technical blueprint for implementing the approved functional scope in Odoo 19.
Use `odoo-19` references to ground ORM, XML, security, testing, and integration decisions.

## Required Inputs
- Approved functional specification from stage 02.
- Acceptance criteria and exception handling definitions.
- Existing module landscape and dependency constraints.
- Non-functional constraints (performance, auditability, compliance).

## Workflow
1. Map each capability to technical components (models, views, actions, security).
2. Define data model changes and module dependencies.
3. Design ACLs, record rules, and role-level access behavior.
4. Specify data files, automation, and integration boundaries.
5. Produce traceability from functional criterion to technical decision.

## Outputs
- Technical design specification with architecture decisions.
- Data model and security design package.
- Functional-to-technical traceability matrix.

## Definition of Done
- Technical decisions are explicit and non-ambiguous.
- Security and data implications are fully documented.
- Implementation teams can build without missing design choices.

## Handoff
Provide the stage output to `$odoo-stage-04-planning` including:
- Approved technical decisions and constraints.
- Estimated complexity by component.
- Identified risks and external dependencies.
