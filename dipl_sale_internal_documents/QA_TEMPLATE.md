# Plantilla QA

## Objetivo

Esta plantilla sirve para ejecutar y registrar la validación funcional de:

- `dipl_doc_sale`
- `dipl_sale_internal_documents`

La idea es usarla directamente en `staging` con datos reales o representativos de producción.

## Datos de ejecución

- Fecha:
- Entorno:
- Rama:
- Base de datos:
- Empresa:
- Probador:
- Idioma de usuario:
- Módulo:
- Versión del módulo:

## Checklist previo

Antes de empezar, verificar:

- módulos actualizados sin errores RPC,
- traducciones cargadas,
- usuario con idioma esperado,
- al menos una cotización y una orden confirmada disponibles,
- al menos un partner en `es_AR`,
- al menos un partner en inglés,
- al menos una orden con líneas técnicas de `dipl_sale_technical_quote`.

## Instrucciones de registro

Para cada caso:

1. completar la acción ejecutada,
2. comparar contra el resultado esperado,
3. marcar estado:
   - `Pass`
   - `Fail`
   - `Blocked`
4. adjuntar evidencia:
   - nombre de PDF,
   - captura,
   - nota de UI,
   - error RPC si aplica
5. dejar observaciones si el resultado fue parcial o ambiguo.

## Ficha de caso de prueba

- ID:
- Escenario:
- Precondiciones:
- Datos usados:
- Acción ejecutada:
- Resultado esperado:
- Resultado obtenido:
- Estado:
  - `Pass`
  - `Fail`
  - `Blocked`
- Evidencia:
- Observaciones:

## Matriz de pruebas

| ID | Módulo | Escenario | Precondiciones | Acción | Resultado esperado | Estado | Evidencia | Observaciones |
|---|---|---|---|---|---|---|---|---|
| T01 | `dipl_doc_sale` | Cotización en español | Partner con `lang = es_AR` | Imprimir cotización | El PDF renderiza en español |  |  |  |
| T02 | `dipl_doc_sale` | Cotización en inglés | Partner con `lang = en_US` o equivalente | Imprimir cotización | El PDF renderiza en inglés |  |  |  |
| T03 | `dipl_doc_sale` | Orden de venta confirmada en español | Orden confirmada, partner `lang = es_AR` | Imprimir orden de venta | El PDF renderiza en español |  |  |  |
| T04 | `dipl_doc_sale` | Vinculación del print estándar | Cualquier cotización/orden | Click en `Imprimir` estándar | Abre el reporte Dipleg, no el default de Odoo |  |  |  |
| T05 | `dipl_doc_sale` | Estructura documental AR | Cualquier documento comercial impreso | Inspección visual del PDF | Header, bloque cliente/meta, tabla, totales y footer correctos |  |  |  |
| T06 | `dipl_sale_internal_documents` | Botones internos ocultos en cotización | `sale.order` en `draft` o `sent` | Abrir formulario | `Lista de corte` y `Orden interna` no son visibles |  |  |  |
| T07 | `dipl_sale_internal_documents` | Botones internos visibles en orden confirmada | `sale.order` en `sale` | Abrir formulario | `Lista de corte` y `Orden interna` son visibles |  |  |  |
| T08 | `dipl_sale_internal_documents` | Botones internos destacados | `sale.order` en `sale` | Abrir formulario | Ambos botones se ven destacados/verdes |  |  |  |
| T09 | `dipl_sale_internal_documents` | Traducción de botones internos | Usuario/sesión en `es_AR` | Abrir orden confirmada | Los botones muestran `Lista de corte` y `Orden interna` |  |  |  |
| T10 | `dipl_sale_internal_documents` | Bloqueo backend en cotización | Intento de ejecutar la acción fuera de orden confirmada | Lanzar acción sobre orden no `sale` | El sistema bloquea la impresión con error de validación |  |  |  |
| T11 | `dipl_sale_internal_documents` | Sin bindings residuales en `Imprimir` | `sale.order` en estado cotización | Abrir menú `Imprimir` genérico | Los documentos internos no aparecen allí |  |  |  |
| T12 | `dipl_sale_internal_documents` | Idioma de `Lista de corte` | Orden confirmada, usuario/sesión `es_AR` | Imprimir `Lista de corte` | El PDF renderiza en español |  |  |  |
| T13 | `dipl_sale_internal_documents` | Idioma de `Orden interna` | Orden confirmada, usuario/sesión `es_AR` | Imprimir `Orden interna` | El PDF renderiza en español |  |  |  |
| T14 | `dipl_sale_internal_documents` | Bloque cliente en `Lista de corte` | Orden confirmada | Imprimir `Lista de corte` | Solo se muestra el nombre del cliente; sin dirección, cond. IVA, CUIT ni vendedor |  |  |  |
| T15 | `dipl_sale_internal_documents` | Bloque fiscal empresa en `Lista de corte` | Orden confirmada | Imprimir `Lista de corte` | No aparece el bloque fiscal derecho del header |  |  |  |
| T16 | `dipl_sale_internal_documents` | Metadata en `Orden interna` | Orden confirmada con vendedor y lista de precios | Imprimir `Orden interna` | Muestra correctamente `Vendedor` y `Lista de precios` |  |  |  |
| T17 | `dipl_sale_internal_documents` | Formato numérico técnico | Orden confirmada con valores técnicos | Imprimir cualquiera de los dos reportes internos | `Desarrollo` y `Largo` sin decimales; `Kilogramos` con 2 decimales |  |  |  |
| T18 | `dipl_sale_internal_documents` | Bloque de checkboxes | Orden confirmada | Imprimir `Orden interna` | Se visualizan `Pago`, `Cliente avisado` y `Entrega` |  |  |  |
| T19 | `dipl_sale_internal_documents` | Importes ocultos en `Lista de corte` | Orden confirmada | Imprimir `Lista de corte` | No aparece bloque de importes/totales |  |  |  |
| T20 | `dipl_sale_internal_documents` | Importes visibles en `Orden interna` | Orden confirmada | Imprimir `Orden interna` | Se muestran subtotal, impuestos y total |  |  |  |
| T21 | Ambos | Seguridad de actualización del módulo | Último código desplegado | Actualizar módulo | No hay errores RPC ni errores de vistas/reportes |  |  |  |
| T22 | Ambos | Seguridad de carga de traducciones | Último `.po` cargado | Actualizar + imprimir | No quedan cadenas en inglés fuera de la política definida |  |  |  |

## Orden recomendado de ejecución

1. `T21`
2. `T06` a `T11`
3. `T12` a `T20`
4. `T01` a `T05`
5. `T22`

## Resumen final

- Casos `Pass`:
- Casos `Fail`:
- Casos `Blocked`:
- Hallazgos críticos:
- Hallazgos menores:
- Riesgos residuales:
- Recomendación:
  - `Apto para continuar`
  - `Apto con observaciones`
  - `No apto`
