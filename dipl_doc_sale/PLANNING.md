# dipl_doc_sale

## Etapa

Análisis y planificación

## Objetivo

Crear un nuevo módulo Odoo 19 enfocado en documentos de ventas para Argentina, basado en `sale.order`.

La primera iteración `V1` queda limitada a una sola salida PDF:

- Cotización formal comercial

Las siguientes iteraciones podrán incorporar:

- Lista de corte
- Orden interna de flujo comercial

El objetivo de negocio inicial es reemplazar el PDF genérico y débil de cotización actual por un documento formal, ordenado y profesional para uso comercial argentino.

## Problema

Los PDFs actuales de cotizaciones y órdenes de venta en Odoo no alcanzan el nivel de presentación comercial esperado.

Necesidad observada:

- las cotizaciones enviadas a clientes deben verse formales y comercialmente serias,
- los operarios necesitan una lista de corte práctica para ejecución en taller,
- el equipo comercial/interno necesita un documento en papel con sectores adicionales para completar manualmente.

En este repositorio ya existe el módulo `dipl_sale_technical_quote`, pero ese módulo resuelve otro problema: lógica de cotización técnica y una capa liviana de presentación sobre el reporte estándar de ventas. No es el límite de ownership correcto para una familia más amplia de documentos comerciales e internos.

## Alcance

### En alcance para V1

- Nuevo módulo independiente: `dipl_doc_sale`
- Modelo raíz de documentos: `sale.order`
- Un único reporte PDF en V1:
  - cotización formal comercial
- Apariencia documental comercial argentina compartida
- Snippets reutilizables compartidos para:
  - encabezado documental,
  - bloque de cliente,
  - bloque de metadata comercial,
  - leyendas legales/comerciales

### Fuera de alcance para V1

- comportamiento fiscal válido de factura,
- CAE, letra fiscal, numeración AFIP o simulación de documento fiscal,
- lista de corte en V1,
- orden interna de flujo comercial en V1,
- automatización de workflow de producción, pago o entrega,
- nuevos modelos persistentes salvo que diseño luego demuestre que son necesarios,
- mezclar este trabajo dentro de `dipl_sale_technical_quote`

## Intención funcional por reporte

### 1. Cotización formal comercial

Audiencia:

- cliente

Propósito:

- comunicar precios, condiciones comerciales, plazos e información formal de la oferta

Énfasis esperado:

- presentación profesional fuerte,
- identidad comercial argentina,
- claridad de datos del cliente,
- validez de la oferta,
- condiciones comerciales,
- buena legibilidad de líneas y totales

## Documentos diferidos a iteraciones posteriores

### 2. Lista de corte

Audiencia:

- operarios / taller

Propósito:

- proveer un documento operativo para ejecución de cortes y plegados

Énfasis esperado:

- legibilidad por encima de estética,
- detalle por línea,
- cantidades,
- medidas,
- notas operativas,
- layout amigable para impresión

### 3. Orden interna de flujo comercial

Audiencia:

- usuarios internos comerciales / administrativos

Propósito:

- replicar la base de la cotización, agregando sectores pensados para completar manualmente en papel

Énfasis esperado:

- misma base comercial de referencia,
- secciones extra de control interno,
- checkboxes manuales o áreas manuscritas para:
  - estado de producción,
  - estado de pago,
  - estado de entrega

## Decisiones del usuario ya capturadas

- Se prefiere un módulo nuevo en lugar de extender `dipl_sale_technical_quote`.
- La `V1` debe cubrir únicamente la cotización formal comercial.
- La lista de corte y la orden interna quedan para iteraciones posteriores.
- El estilo documental debe inspirarse en la presentación argentina de la Factura A.
- El objetivo es formalidad comercial argentina, no validez fiscal/legal de factura.

## Resumen del benchmark

### Fuentes analizadas

- `.src/odoo`
- `.src/adhoc-sale`
- `.src/adhoc-sale-argentina`

### Hallazgos relevantes

#### Odoo estándar

La base estándar de documentos de ventas sigue siendo genérica y está centrada en la plantilla estándar del reporte de ventas y el contenido portal. Sirve como base técnica, pero no alcanza como presentación comercial argentina final.

Fuente local relevante:

- `.src/odoo/addons/sale/views/sale_portal_templates.xml`

#### Capa genérica de ventas de Adhoc

`sale_ux` agrega mejoras genéricas de reporte, como imágenes opcionales de producto, pero no es la fuente principal del estilo documental argentino.

Fuente local relevante:

- `.src/adhoc-sale/sale_ux/views/sale_reports.xml`

#### Localización argentina de ventas de Adhoc

`l10n_ar_sale` es el benchmark más relevante para comportamiento documental argentino sobre ventas.

Hallazgos clave:

- redirige los reportes de venta AR a una plantilla específica de localización,
- usa `l10n_ar.custom_header`,
- introduce una leyenda comercial: `Invalid document as invoice`,
- define un bloque más formal de cliente y metadata,
- incluye lógica de discriminación de IVA para algunos casos comerciales.

Fuentes locales relevantes:

- `.src/adhoc-sale-argentina/l10n_ar_sale/models/sale_order.py`
- `.src/adhoc-sale-argentina/l10n_ar_sale/views/sale_report_templates.xml`

#### Layout de factura AR de Odoo

La referencia estructural real para el encabezado documental argentino es `l10n_ar.custom_header`.

Fuente local relevante:

- `.src/odoo/addons/l10n_ar/views/report_invoice.xml`

## Decisión del benchmark

### Adoptar

- El patrón estructural de `l10n_ar.custom_header`
- La idea de una leyenda comercial clara y no fiscal
- La composición reutilizable de documentos con estilo argentino

### Extender

- Una familia de reportes propia de Dipleg sobre `sale.order`
- Un primer reporte propio para cotización comercial con arquitectura preparada para crecer luego
- Un sistema documental que diferencie salidas para cliente y salidas internas

### Inspirar

- El bloque cliente y la organización de metadata de `l10n_ar_sale`
- Las convenciones de encabezado comercial argentino
- Patrones de documentos operativos internos tomados de reportes AR relacionados

### Descartar

- Dependencia directa del módulo completo `l10n_ar_sale` como requisito duro de arquitectura
- Reutilización literal de semántica fiscal de factura
- Embutir este trabajo en `dipl_sale_technical_quote`

## Dirección arquitectónica

### Nombre técnico recomendado

`dipl_doc_sale`

### Límite de ownership recomendado

Este módulo debe ser dueño del render documental de PDFs comerciales e internos basados en `sale.order`.

No debe ser dueño de:

- lógica de pricing técnico de productos,
- comportamiento fiscal de factura,
- gestión de workflow de producción en taller

### Forma de diseño recomendada

- modelo base: `sale.order`
- una primera `ir.actions.report`
- una primera plantilla QWeb de cotización, preparada para futuras variantes
- snippets compartidos para estructura común
- dependencias mínimas al inicio

### Postura inicial sobre dependencias

Dependencia mínima esperada:

- `sale_management`

Posible dependencia opcional más adelante, solo si diseño lo requiere:

- módulos técnicos que enriquezcan los datos de la lista de corte

Esto queda pendiente hasta que la etapa de diseño confirme si la lista de corte depende de campos hoy propios de `dipl_sale_technical_quote`.

## Riesgos principales

### 1. Riesgo de confusión fiscal

Si la cotización comercial imita demasiado literalmente a una factura A, el PDF resultante puede generar confusión fiscal.

Control:

- mantener una leyenda no fiscal,
- evitar CAE,
- evitar letra fiscal presentada como si fuera una factura válida,
- evitar semántica AFIP salvo requerimiento explícito y jurídicamente justificado

### 2. Riesgo de límite de ownership

Si este trabajo documental se mezcla con `dipl_sale_technical_quote`, el límite del módulo queda difuso y el mantenimiento futuro se complica.

Control:

- mantener `dipl_doc_sale` independiente

### 3. Riesgo de expansión de alcance

La cotización puede contaminarse si en la misma iteración intentamos resolver también necesidades operativas o administrativas internas.

Control:

- mantener `V1` enfocada solo en el documento comercial para cliente,
- dejar lista de corte y orden interna para iteraciones posteriores

## Criterios de éxito

La etapa de planificación se considerará satisfecha si la implementación posterior entrega:

- un módulo nuevo claramente separado de `dipl_sale_technical_quote`,
- una cotización formal comercial claramente superior al PDF estándar de Odoo,
- una presentación comercial argentina reconocible,
- ausencia de simulación de factura fiscal válida,
- composición QWeb compartida y trazable,
- una `V1` acotada, centrada en el documento comercial y no en convertirse en proyecto de workflow

## Preguntas abiertas para Diseño

Estos puntos quedan para decidir en la siguiente etapa:

- XML IDs exactos de reportes y nombres de archivos,
- desglose exacto de snippets QWeb,
- si la cotización debe mostrar IVA discriminado o no como política comercial,
- si las acciones de reporte deben convivir con el PDF estándar de cotización o reemplazarlo en algunos flujos

Preguntas ya diferidas para próximas iteraciones:

- si la lista de corte consume solo líneas estándar de venta o también campos técnicos/custom,
- si la orden interna requiere solo checkboxes impresos estáticos o luego campos digitales

## Siguiente etapa

Diseño

Salida esperada de la siguiente etapa:

- estructura técnica del módulo,
- decisión de manifest y dependencias,
- mapa de la acción de reporte de cotización,
- arquitectura de templates compartidos para la cotización,
- mapeo de campos de la cotización,
- definición del slice de implementación V1
