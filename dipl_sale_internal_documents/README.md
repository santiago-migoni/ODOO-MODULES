# Sales Internal Documents

`dipl_sale_internal_documents` is an Odoo 19 custom module that adds internal printable documents over `sale.order`.

## Current Scope

The current `V1` introduces two internal document flows:

- cutting list,
- internal order.

It still does not include:

- persisted internal workflow fields,
- digital checkbox tracking,
- stock or production workflow automation,
- replacement of standard commercial quotation documents.

## Purpose

The goal of the module is to provide internal sales documents that keep the same documentary family as `dipl_doc_sale` while serving operational and administrative users.

Current policy:

- same visual family as `dipl_doc_sale`,
- internal and non-client-facing use,
- technical line data sourced from `dipl_sale_technical_quote`,
- separate document actions from the commercial sales document flow.

## Dependencies

- `sale_management`
- `dipl_sale_technical_quote`
- `l10n_ar`

## Functional Flow

1. Confirm a sales order.
2. Use one of the internal print actions:
   - `Cutting List`
   - `Internal Order`
3. Generate a PDF with:
   - Dipleg documentary header family,
   - customer block on the left and internal metadata on the right,
   - technical line data from `sale.order.line`,
   - internal-purpose layout.

## Document Policy

These are internal work documents.

Rules:

- they keep the same documentary harmony as `dipl_doc_sale`,
- they do not replace the commercial sales document,
- they do not add persisted business workflow logic in `V1`,
- printed checkboxes are visual only in `V1`.

## Technical Data Source

The module relies on technical sales-line fields introduced by `dipl_sale_technical_quote`:

- `dipl_development_mm`
- `dipl_width_mm`
- `dipl_kg_total`

## Current Documents

### Cutting List

Operational document for shop-floor execution.

Main columns:

- description,
- quantity,
- development,
- length,
- kilograms.

### Internal Order

Administrative internal document for order follow-up.

Main additions over the technical lines:

- line amount and totals,
- pricelist used on the sales order,
- printed process checkboxes.

## Future Iterations

Future iterations may introduce:

- persisted workflow checkboxes,
- additional internal process states,
- tighter reuse of shared Dipleg documentary layout components.
