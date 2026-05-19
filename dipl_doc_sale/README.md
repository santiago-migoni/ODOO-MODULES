# Sales Commercial Documents

`dipl_doc_sale` is an Odoo 19 custom module focused on Argentine-style sales documents over `sale.order`.

## Current Scope

The current `V1` introduces a single new document flow:

- formal commercial quotation.

It still does not include:

- cutting list,
- internal commercial flow order,
- operational or administrative workflow,
- fiscal invoice behavior.

## Purpose

The goal of the module is to replace the weak default quotation PDF with a formal, orderly, and professional document for Argentine commercial use.

Current policy:

- near-mirror structure of Argentine invoice and purchase documents,
- clear commercial presentation,
- explicitly non-fiscal document semantics,
- documentary ownership separated from `dipl_sale_technical_quote`.

## Dependencies

- `sale_management`
- `l10n_ar`

It still avoids direct dependency on:

- `l10n_ar_sale`,
- `l10n_ar_tax`,
- `sale_ux`.

## Functional Flow

1. Create or open a sales quotation or order.
2. Use the `Dipleg Commercial Quotation` print action.
3. Generate a PDF with:
   - Argentine-style documentary header,
   - customer block on the left and commercial metadata on the right,
   - line table aligned with invoice/purchase document structure,
   - totals block aligned with the AR pattern,
   - non-fiscal legend.

## Documentary Policy

The document follows a near-mirror structure of formal Argentine documents, but does not simulate a valid invoice.

Rules:

- keeps an explicit quotation / sales-order title,
- avoids CAE and fiscal numbering,
- avoids presenting a fiscal-valid document letter,
- keeps a non-fiscal documentary legend.

## Relation to Other Modules

`dipl_doc_sale` does not replace the technical pricing logic of `dipl_sale_technical_quote`.

If an order contains technical information coming from other modules, this module can still render the sales document, but it does not own the technical calculation logic.

## Future Iterations

Future iterations may introduce:

- cutting list,
- internal commercial flow order,
- additional documentary reuse patterns.
