# Technical Design

## Module

- Technical name: `dipl_sale_internal_documents`
- Stage: Design
- Status: Approved for scaffolding after field-name verification

## Goal

Provide two internal `sale.order` printable documents that reuse the same visual family as `dipl_doc_sale` while serving different internal audiences:

1. `Cutting List`
2. `Internal Sales Order`

This module is not client-facing. It must keep documentary harmony with `dipl_doc_sale`, but it does not need the explicit non-fiscal `X / Invalid document as invoice` center legend.

## Business Intent

### Cutting List

- Audience: shop-floor operators
- Trigger: confirmed work
- Purpose: execute cutting work
- Critical data per line:
  - development
  - length
  - weight

### Internal Sales Order

- Audience: administrative team
- Trigger: confirmed work
- Purpose: follow the order lifecycle from intake to closure
- Critical data per line:
  - development
  - length
  - weight
- Additional requirement:
  - printed checkbox block for internal tracking

## Source Models

- Root model: `sale.order`
- Line model: `sale.order.line`

Technical fields already exist on `sale.order.line` and come from `dipl_sale_technical_quote`.

The exact technical field names still need to be verified during development before wiring the templates.

## Dependencies

- `sale_management`
- `dipl_sale_technical_quote`

No dependency on `dipl_doc_sale` is required at manifest level for `V1`.

`dipl_doc_sale` is a visual benchmark, not a functional dependency.

## Visual Policy

This module must reuse the same documentary grammar as `dipl_doc_sale`.

That means:

- same overall header composition
- same company / customer / metadata rhythm
- same table density and alignment logic
- same documentary seriousness and spacing

This module should not invent a new family of internal reports.

### Explicit rule

Take `dipl_doc_sale` as the direct visual reference and add internal-purpose features on top of that structure.

## V1 Scope

### Report 1: Cutting List

Purpose:

- operational execution document

Structure:

1. Header
   - title: `CUTTING LIST`
   - order number
   - order date
   - customer

2. Company / customer / metadata block
   - mirror the `dipl_doc_sale` structure
   - simplify metadata to what operators need

3. Main table
   - line description
   - quantity
   - development
   - length
   - weight

4. Footer
   - optional notes
   - page counter

Design rule:

- prioritize compactness and readability
- no totals are required unless business later proves they help the operators

### Report 2: Internal Sales Order

Purpose:

- internal administrative tracking document

Structure:

1. Header
   - title: `INTERNAL SALES ORDER`
   - order number
   - order date
   - customer

2. Company / customer / metadata block
   - same visual family as `dipl_doc_sale`
   - metadata should include:
     - salesperson
     - customer reference
     - payment terms if present
     - delivery date if present

3. Main table
   - line description
   - quantity
   - development
   - length
   - weight
   - optional subtotal only if administrative users confirm it adds value

4. Internal process block
   - printed checkboxes only in `V1`
   - initial set:
     - `Payment`
     - `Customer Notified`
     - `Delivery`

5. Footer
   - optional internal notes
   - page counter

## Out of Scope for V1

- new persisted workflow fields
- digital workflow tracking
- automatic process state computation
- production planning logic
- stock integration
- replacing standard reports

## Recommended File Structure

- `dipl_sale_internal_documents/__manifest__.py`
- `dipl_sale_internal_documents/__init__.py`
- `dipl_sale_internal_documents/README.md`
- `dipl_sale_internal_documents/CHANGELOG.md`
- `dipl_sale_internal_documents/report/internal_document_actions.xml`
- `dipl_sale_internal_documents/report/internal_document_templates.xml`

`models/` is not required for `V1` unless runtime report routing or helper methods become necessary.

## Report Strategy

Use new report actions, not standard report replacement.

Rationale:

- safer rollout
- no collision with the commercial client-facing document flow
- easier validation with internal users

## Reuse Strategy

### Adopt from `dipl_doc_sale`

- documentary visual family
- high-level report composition
- company / customer / metadata rhythm
- document density and alignment rules

### Extend for internal use

- technical columns from `dipl_sale_technical_quote`
- internal checkbox block
- internal-purpose titles

### Do not copy blindly

- the `X / Invalid document as invoice` center legend is not required by default here
- client-facing non-fiscal semantics are not the primary concern

## Open Technical Questions

1. Exact technical field names on `sale.order.line` for:
   - development
   - length
   - weight

2. Whether `Internal Sales Order` should show commercial amounts in `V1`

3. Whether line description should render from:
   - `line.name`
   - or a more structured technical composition

## Implementation Order

1. Verify exact technical field names from `dipl_sale_technical_quote`
2. Scaffold `dipl_sale_internal_documents`
3. Implement `Cutting List`
4. Validate data density and usability
5. Implement `Internal Sales Order`
6. Validate checkbox block and administrative readability

## Risks

### Data risk

If technical fields are not consistently populated on all sales lines, the reports may look incomplete.

### Drift risk

If the templates are implemented without a strict `dipl_doc_sale` benchmark pass, the internal documents may drift into a different visual family.

### Scope risk

If checkbox requirements evolve into persisted workflow states, `V2` will need models and stored fields, not just printable documents.

## Definition of Done for V1

- `Cutting List` renders from `sale.order`
- `Internal Sales Order` renders from `sale.order`
- both use technical line data from `dipl_sale_technical_quote`
- both visually belong to the same document family as `dipl_doc_sale`
- checkbox block exists on the internal order as printed marks only
- no client-facing commercial document behavior is affected
