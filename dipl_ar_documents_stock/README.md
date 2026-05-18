# Dipleg AR Documents Stock

Adaptador formal AR para documentos de `stock.picking` dentro del framework `dipl_ar_documents`.

## Proposito

Este addon toma control del flujo principal de impresion de stock para estandarizar:

- delivery slip,
- goods receipt note,
- internal move base,
- return slip con header/footer Dipleg.

## Dependencias

- `dipl_ar_documents`
- `stock`

## Estado funcional actual

El addon ya incluye:

- activacion por compania AR,
- toma de control de `stock.report_delivery_document`,
- header y footer AR Dipleg sobre delivery y receipt,
- bloque documental formal para contraparte, direccion operativa y metadata,
- header/footer Dipleg sobre `Return slip`,
- smoke tests HTML para outgoing, incoming y return.
