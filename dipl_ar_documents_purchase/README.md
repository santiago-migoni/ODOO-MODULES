# Dipleg AR Documents Purchase

Adaptador de compras para el framework `dipl_ar_documents`.

## Proposito

Este addon conectara la capa comun Dipleg con los reportes de `purchase.order`:

- request for quotation,
- purchase order.

## Dependencias

- `dipl_ar_documents`
- `purchase`

## Estado funcional actual

El addon ya incluye:

- routing AR explicito para reportes de `purchase.order`,
- templates Dipleg iniciales para RFQ y purchase order,
- reutilizacion del header emisor comun, footer pager y helpers del core `dipl_ar_documents`,
- separacion visual consistente entre header, bloque informativo y tabla principal,
- supresion basica de campos vacios en informacion complementaria,
- smoke tests HTML para RFQ y purchase order.
