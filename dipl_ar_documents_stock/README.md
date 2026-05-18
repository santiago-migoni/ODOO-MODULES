# Dipleg AR Documents Stock

Adaptador formal AR para documentos de `stock.picking` dentro del framework `dipl_ar_documents`.

## Proposito

Este addon toma control del flujo principal de impresion de stock para estandarizar:

- delivery slip,
- goods receipt note,
- internal move.

## Dependencias

- `dipl_ar_documents`
- `stock`

## Estado funcional actual

El addon ya incluye:

- activacion por compania AR,
- toma de control de `stock.report_delivery_document`,
- header y footer AR Dipleg sobre delivery, receipt e internal move,
- bloque documental formal para contraparte, direccion operativa y metadata,
- smoke tests HTML para outgoing, incoming e internal.

## Fuera de V1

- `Picking Operations`
- `Return slip`
