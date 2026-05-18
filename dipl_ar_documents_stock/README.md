# Dipleg AR Documents Stock

Adaptador de stock para el framework `dipl_ar_documents`.

## Proposito

Este addon conecta la capa comun Dipleg con el documento AR de stock definido por `l10n_ar_stock`:

- remito / delivery guide

## Dependencias

- `dipl_ar_documents`
- `l10n_ar_stock`

## Estado

Stage 06 implementado para el documento AR de remito sobre la base de `l10n_ar_stock`.

## Validacion actual

- activacion condicional por compania AR y numero de remito,
- smoke test HTML del delivery guide localizado.
