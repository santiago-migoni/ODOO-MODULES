---
name: odoo-design
description: Design workflow for Odoo custom module delivery. Use when turning approved problem framing into a concrete technical design covering models, views, security, data, dependencies, module strategy, and implementation structure.
---

# Odoo Design

## Overview
Define the solution before coding starts.
Use this skill to translate approved scope into a technical design that is precise enough to guide implementation without leaving core architecture decisions unresolved.
Use `odoo-19` as the primary technical reference.
Use `odoo-project-management` only when design tradeoffs materially affect release scope, backlog order, or iteration sequencing.

## Required Inputs
- Stable analysis and planning package from `odoo-analysis-planning`.
- Business rules, success criteria, and scope boundaries.
- Known constraints around integrations, performance, security, and maintainability.
- Current module landscape and dependency assumptions.

## Workflow
1. Define the solution architecture and the module strategy for the requested scope.
2. Design models, fields, views, access rules, data files, automation, and integration points.
3. Make explicit structural decisions such as reuse, extension, or new-module boundaries.
4. Identify implementation slices, dependency order, and scaffolding implications.
5. Record design risks, tradeoffs, and compatibility assumptions.
6. Route to `odoo-coding` once the solution is technically coherent and implementation-ready.

## Outputs
- Technical design package for models, views, security, data, and integrations.
- Module strategy and structural decisions.
- Implementation-slice outline with dependency order.
- Design risk and tradeoff log.

## Definition of Done
- Core technical decisions are explicit and internally coherent.
- Implementation can start without architecture-level guessing.
- Dependency order and structural boundaries are clear.
- The next handoff to coding is explicit.

## Handoff
- Hand off to `odoo-coding` when the solution is implementation-ready.
- Hand off to `odoo-project-management` when scope, release order, or sequencing must be adjusted based on design findings.
- Hand off back to `odoo-analysis-planning` when the design exposes unresolved business ambiguity or invalid scope assumptions.

## Related References
- Use `references/design-deliverable-template.md` for the main technical design output.
