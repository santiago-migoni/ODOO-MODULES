# Dipleg AR Documents Sale

Adaptador de ventas para el framework `dipl_ar_documents`.

## Proposito

Este addon conectara la capa comun Dipleg con los reportes de `sale.order`:

- cotizaciones,
- ordenes de venta,
- pro-forma si luego entra en alcance.

## Dependencias

- `dipl_ar_documents`
- `sale_management`

## Estado funcional actual

El addon ya incluye:

- routing AR explicito para `sale.report_saleorder_document`,
- herencia de wrappers de venta para quotation y pro-forma,
- template Dipleg inicial para cotizacion y orden de venta,
- reutilizacion del header emisor comun, footer pager y helpers del core `dipl_ar_documents`,
- smoke tests HTML para quotation, sales order y pro-forma.
