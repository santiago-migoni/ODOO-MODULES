# Documentos comerciales de ventas

`dipl_doc_sale` es un módulo custom para Odoo 19 orientado a la presentación documental de ventas sobre `sale.order`.

## Alcance actual

La `V1` del módulo incorpora un único documento nuevo:

- cotización formal comercial.

No incluye todavía:

- lista de corte,
- orden interna de flujo comercial,
- workflow operativo o administrativo,
- comportamiento fiscal de factura.

## Propósito

El objetivo del módulo es reemplazar la debilidad visual del PDF estándar de cotización con un documento más formal, ordenado y profesional para contexto comercial argentino.

La política actual es:

- inspiración visual argentina,
- presentación comercial clara,
- documento explícitamente no fiscal,
- ownership documental separado de `dipl_sale_technical_quote`.

## Dependencias

- `sale_management`

No depende en esta iteración de:

- `l10n_ar_sale`,
- `l10n_ar_tax`,
- `sale_ux`.

## Flujo funcional

1. Crear o abrir una cotización en Ventas.
2. Usar la nueva acción de impresión `Cotización comercial Dipleg`.
3. Obtener un PDF con:
   - encabezado comercial formal,
   - bloque cliente ordenado,
   - metadata comercial,
   - tabla de líneas más legible,
   - totales reforzados,
   - leyenda no fiscal.

## Política documental

La cotización está inspirada en la jerarquía visual de documentos argentinos tipo factura, pero no simula una factura válida.

Reglas:

- mantiene título explícito de cotización,
- evita CAE y numeración fiscal,
- evita letra fiscal presentada como válida,
- conserva una leyenda documental no fiscal.

## Relación con otros módulos

`dipl_doc_sale` no reemplaza la lógica técnica de `dipl_sale_technical_quote`.

Si una orden contiene información técnica proveniente de otros módulos, este módulo puede renderizar la orden comercialmente, pero no asume ownership del cálculo técnico.

## Iteraciones futuras

Las siguientes iteraciones podrán incorporar:

- lista de corte,
- orden interna de flujo comercial,
- reutilización de snippets documentales compartidos.
