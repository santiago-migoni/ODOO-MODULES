# Backlog

## Purpose

This backlog captures the remaining work after the architectural refactor of
`dipl_doc_sale`.

The current module already aligns with the main `l10n_ar` and
`l10n_ar_purchase` patterns at the architecture level:

- report routing exists on `sale.order`,
- the main document inherits `sale.report_saleorder_document`,
- the report reuses the `l10n_ar` header pattern,
- the report uses `custom_footer`,
- document naming already changes by state.

The remaining work is now detail-oriented. The gaps are mostly about document
policy, block content, and visual parity.

## Backlog Items

### P1. Decide delivery-address visibility

Status:
- pending

Problem:
- The report already shows `Delivery Date` and `Incoterm`.
- It does not show a dedicated delivery or shipping address block.

Benchmark reference:
- `l10n_ar_purchase` gives explicit visibility to shipping data when that
  information matters operationally.

Decision needed:
- show no delivery address,
- show the shipping address always,
- or show the shipping address only when it differs from the commercial
  customer.

Implementation target:
- [quote_report_templates.xml](/Users/santiago_migoni/Documents/Codex/report/dipl_doc_sale/report/quote_report_templates.xml)

Done when:
- the document policy is explicit,
- the chosen address rule is implemented,
- the layout remains stable for both quotation and sales order states.

### P1. Refine VAT label rendering

Status:
- pending

Problem:
- The current report prints taxes using generic labels from `tax_label` or
  `name`.

Benchmark reference:
- `l10n_ar` and `l10n_ar_purchase` present VAT with tighter control and more
  predictable documentary output.

Decision needed:
- show only VAT taxes,
- show all tax labels,
- or normalize the output to a simpler `% VAT` presentation.

Implementation target:
- [quote_report_templates.xml](/Users/santiago_migoni/Documents/Codex/report/dipl_doc_sale/report/quote_report_templates.xml)

Done when:
- tax labels are deterministic,
- the line column remains readable,
- and the output matches the intended Argentine commercial style.

### P1. Refine state-specific right-column metadata

Status:
- pending

Problem:
- The report already changes `report_name` and the header date label by
  `sale.order.state`.
- The right-side metadata block still uses nearly the same structure for all
  states.

Benchmark reference:
- `l10n_ar_purchase` changes documentary emphasis depending on whether the
  document is still a quotation or already a confirmed order.

Decision needed:
- for `draft` and `sent`, prioritize `Validity Date`, `Salesperson`,
  `Your Reference`,
- for `sale`, prioritize `Order Date`, `Delivery Date`, `Payment Terms`,
- for `cancel`, confirm whether the metadata block needs cancellation-specific
  emphasis.

Implementation target:
- [quote_report_templates.xml](/Users/santiago_migoni/Documents/Codex/report/dipl_doc_sale/report/quote_report_templates.xml)

Done when:
- quotation and sales order states feel like different business documents,
- but they still belong to the same documentary family.

### P2. Review header address source

Status:
- pending

Problem:
- The report currently uses `doc.company_id.partner_id` as `header_address`.

Benchmark reference:
- `l10n_ar` uses a fiscal or point-of-sale-oriented address source.
- `l10n_ar_purchase` uses the company partner.

Decision needed:
- keep the company commercial address,
- introduce a dedicated documentary address source,
- or prepare a future sales-document address policy.

Implementation target:
- [quote_report_templates.xml](/Users/santiago_migoni/Documents/Codex/report/dipl_doc_sale/report/quote_report_templates.xml)
- [sale_order.py](/Users/santiago_migoni/Documents/Codex/report/dipl_doc_sale/models/sale_order.py)

Done when:
- the address source is intentionally chosen,
- and the header prints the correct company identity for the intended business
  use.

### P2. Review company identity detail level

Status:
- pending

Problem:
- The header already prints company name, address, contact data, and CUIT.
- It does not yet decide whether additional company identity data should be
  shown.

Benchmark reference:
- `l10n_ar` prints a stronger fiscal identity block.

Decision needed:
- keep the current lighter commercial identity,
- or add selected company fields such as VAT responsibility when useful for
  commercial formality.

Implementation target:
- [quote_report_templates.xml](/Users/santiago_migoni/Documents/Codex/report/dipl_doc_sale/report/quote_report_templates.xml)

Done when:
- the company block has the intended level of legal-commercial formality,
- without making the quotation look like a fiscal invoice.

### P2. Review totals presentation

Status:
- pending

Problem:
- Totals are currently rendered from `sale.document_tax_totals`.

Benchmark reference:
- The AR document family tends to present totals with slightly stricter visual
  hierarchy and documentary weight.

Decision needed:
- keep the current totals data source and adjust only styling,
- or refine labels and row ordering without introducing fiscal invoice logic.

Implementation target:
- [quote_report_templates.xml](/Users/santiago_migoni/Documents/Codex/report/dipl_doc_sale/report/quote_report_templates.xml)

Done when:
- the totals block is visually consistent with the AR documentary family,
- while keeping standard sales logic.

### P3. Run side-by-side visual QA against AR invoice and AR purchase documents

Status:
- pending

Problem:
- Structural alignment has been reviewed from source code.
- Visual parity has not yet been validated in live Odoo rendering.

Comparison set:
- `l10n_ar` invoice PDF,
- `l10n_ar_purchase` purchase quotation or purchase order PDF,
- `dipl_doc_sale` quotation or sales order PDF.

Review focus:
- spacing,
- alignment,
- typography,
- hierarchy,
- metadata density,
- line table balance,
- totals balance.

Done when:
- a side-by-side runtime review is completed,
- and any visual mismatches are converted into implementation tasks or closed
  as acceptable differences.

### P3. Review final user-facing wording

Status:
- pending

Problem:
- The current coded labels are in English, following the implementation rule.
- The end-user document language still needs an explicit product decision.

Decision needed:
- keep English labels in the printed document,
- or translate the visible report wording for the target operating audience.

Focus areas:
- `Invalid document as invoice`,
- footer legend,
- report action visible name,
- state-based document titles.

Implementation target:
- [quote_report_templates.xml](/Users/santiago_migoni/Documents/Codex/report/dipl_doc_sale/report/quote_report_templates.xml)
- [quote_report_actions.xml](/Users/santiago_migoni/Documents/Codex/report/dipl_doc_sale/report/quote_report_actions.xml)
- [es_AR.po](/Users/santiago_migoni/Documents/Codex/report/dipl_doc_sale/i18n/es_AR.po)

Done when:
- the report language policy is explicit,
- and the visible wording is consistent with that policy.

## Explicitly Deferred

The following items are intentionally out of scope for this backlog because
they belong to later functional iterations:

- cutting list,
- internal commercial flow order,
- persistent workflow fields,
- production, payment, and delivery checkbox flows,
- fiscal invoice behavior,
- advanced tax recomputation logic.
