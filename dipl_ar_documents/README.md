# Dipleg AR Documents

Modulo base para estandarizar documentos internos imprimibles de Dipleg en companias AR.

## Proposito

Este addon define la capa comun para:

- contrato QWeb compartido,
- helpers de activacion y politica documental,
- bloques reutilizables de header, footer e identidad documental.

## Alcance V1

El modulo base no adapta por si mismo documentos de ventas, compras o stock.

Los adaptadores funcionales viven en:

- `dipl_ar_documents_sale`
- `dipl_ar_documents_purchase`
- `dipl_ar_documents_stock`

## Dependencias

- `l10n_ar`

## Estado

Stage 06 implementado como core reusable para templates y helpers AR.

## Validacion actual

- tests del core sobre activacion AR y helpers comunes,
- coverage de render delegada a los adaptadores funcionales.
