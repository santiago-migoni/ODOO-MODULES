# dipl_doc_sale

## Etapa

Diseño

## Objetivo de la iteración

Implementar una `V1` acotada de `dipl_doc_sale` para generar una cotización formal comercial argentina sobre `sale.order`, sin simular una factura fiscal y sin mezclar esta entrega con documentos internos u operativos.

## Alcance de V1

### En alcance

- Nuevo módulo `dipl_doc_sale`
- Un reporte PDF nuevo para cotización formal comercial
- Layout comercial argentino inspirado en la Factura A
- Reutilización de `sale.order` y `sale.order.line`
- Arquitectura QWeb preparada para crecer en iteraciones futuras
- Leyenda documental no fiscal

### Fuera de alcance

- Lista de corte
- Orden interna de flujo comercial
- Campos nuevos de workflow
- Persistencia de estados internos
- Simulación de factura fiscal
- CAE, letra fiscal válida, códigos AFIP o semántica tributaria de factura
- Cambios a `dipl_sale_technical_quote`

## Estrategia de módulo

### Decisión estructural

Se implementará un módulo nuevo, independiente de `dipl_sale_technical_quote`, porque:

- el problema actual es documental, no de pricing técnico,
- la ownership del layout debe quedar aislada,
- la arquitectura debe permitir sumar luego otros documentos sin contaminar módulos funcionalmente ajenos.

### Módulo objetivo

`dipl_doc_sale`

### Dependencia inicial

- `sale_management`

### Dependencias explícitamente evitadas en V1

- `l10n_ar_sale`
- `l10n_ar_tax`
- `sale_ux`

Motivo:

- son referencias útiles para benchmark y diseño,
- pero no deben convertirse en dependencia dura para una primera iteración documental simple.

## Estrategia de reporte

### Decisión principal

La `V1` no debe reemplazar inmediatamente el PDF estándar de cotización.

Se creará una nueva `ir.actions.report` específica para la cotización formal comercial Dipleg.

### Motivo

- reduce riesgo de regresión,
- permite comparación funcional entre el PDF estándar y el nuevo PDF,
- deja margen para validar el layout comercial antes de decidir si más adelante debe sustituir el estándar.

### Evolución posible

En una iteración posterior se podrá decidir:

- convivir permanentemente con el reporte estándar,
- reemplazar el reporte estándar,
- o enrutar condicionalmente según contexto o política comercial.

## Modelo y datos

### Modelo raíz

`sale.order`

### Modelos secundarios

- `sale.order.line`

### Decisión de datos

No se crearán nuevos modelos ni nuevos campos persistentes en `V1`.

La cotización utilizará únicamente datos ya disponibles en ventas, por ejemplo:

- número del documento,
- fecha de pedido,
- fecha de validez,
- cliente,
- vendedor,
- referencia del cliente,
- líneas del pedido,
- impuestos,
- subtotales,
- total,
- términos de pago,
- observaciones / notas.

## Arquitectura QWeb

## Plantilla principal

Se propone una plantilla principal:

- `dipl_doc_sale.report_saleorder_formal_quote_document`

Responsabilidad:

- ensamblar el documento completo,
- invocar snippets compartidos,
- iterar líneas,
- renderizar totales y notas.

## Snippets compartidos

Se propone separar la plantilla en componentes reutilizables:

- `dipl_doc_sale.snippet_formal_header`
- `dipl_doc_sale.snippet_formal_customer_block`
- `dipl_doc_sale.snippet_formal_meta_block`
- `dipl_doc_sale.snippet_formal_lines_table`
- `dipl_doc_sale.snippet_formal_totals`
- `dipl_doc_sale.snippet_formal_legal_legend`

### Objetivo de esta separación

- mantener trazabilidad,
- facilitar mantenimiento,
- permitir reutilización en futuras `V2` y `V3`,
- evitar una plantilla QWeb monolítica difícil de evolucionar.

## Dirección visual y documental

### Inspiración permitida

La cotización debe inspirarse en la lógica visual de una Factura A argentina:

- jerarquía fuerte en encabezado,
- separación clara entre emisor y cliente,
- metadata alineada y ordenada,
- tabla con lectura limpia,
- bloque de totales visualmente fuerte,
- leyenda documental visible.

### Límites obligatorios

La cotización no debe parecer una factura válida.

Por lo tanto, se debe evitar:

- CAE,
- letra fiscal presentada como válida,
- códigos AFIP,
- numeración o bloques que induzcan a pensar que es una factura tributaria,
- terminología fiscal que exceda una cotización comercial.

### Leyenda recomendada

Se debe incluir una leyenda documental no fiscal, por ejemplo:

- `Documento no válido como factura`

La redacción exacta puede cerrarse en implementación, pero la intención es obligatoria.

## Contenido funcional del PDF

### Encabezado empresarial

Debe incluir:

- logo de la empresa si existe,
- nombre legal o comercial,
- CUIT si está disponible y se decide mostrar,
- domicilio comercial,
- teléfono,
- email,
- sitio web si existe.

### Identidad documental

Debe incluir:

- título principal `Cotización`,
- número de cotización,
- fecha de emisión.

Puede incluir:

- una marca documental propia de Dipleg,
- una leyenda secundaria no fiscal.

### Bloque cliente

Debe incluir:

- nombre o razón social,
- domicilio,
- identificación impositiva o documento si ya está disponible en el partner,
- condición frente a IVA si existe y si se decide mostrar.

### Metadata comercial

Debe incluir, cuando exista:

- vendedor,
- fecha de validez,
- referencia del cliente,
- condición de pago,
- plazo o fecha de entrega si está disponible en la orden.

### Tabla de líneas

Debe incluir:

- descripción,
- cantidad,
- unidad de medida,
- precio unitario,
- descuento, si aplica,
- subtotal o total por línea según política definida,
- impuestos, solo si se decide mostrarlos.

### Bloque de totales

Debe incluir:

- subtotal,
- impuestos,
- total final.

### Notas y condiciones

Debe incluir, si existen:

- términos y condiciones,
- observaciones comerciales,
- nota del pedido.

## Política de IVA para V1

### Decisión recomendada

Mantener el comportamiento estándar de Odoo en `V1`.

### Motivo

- evita incorporar lógica tributaria adicional,
- reduce el riesgo de acoplar el diseño a la implementación de `l10n_ar_sale`,
- mantiene la iteración enfocada en calidad documental.

### Consecuencia

La cotización formal comercial `V1` mejora layout y presentación, pero no redefine todavía la política comercial de discriminación de IVA.

Si Dipleg luego decide que la cotización debe discriminar IVA explícitamente, eso debe tratarse como decisión funcional separada.

## Acciones de reporte

### Acción nueva

Se creará una acción nueva de reporte PDF sobre `sale.order`.

Nombre sugerido:

- `Cotización comercial Dipleg`

XML ID sugerido:

- `dipl_doc_sale.action_report_saleorder_formal_quote`

Template sugerido:

- `dipl_doc_sale.report_saleorder_formal_quote`

Documento principal sugerido:

- `dipl_doc_sale.report_saleorder_formal_quote_document`

## Estructura técnica propuesta

### Archivos mínimos del módulo

- `dipl_doc_sale/__init__.py`
- `dipl_doc_sale/__manifest__.py`
- `dipl_doc_sale/README.md`
- `dipl_doc_sale/CHANGELOG.md`
- `dipl_doc_sale/report/__init__.py`
- `dipl_doc_sale/report/quote_report_actions.xml`
- `dipl_doc_sale/report/quote_report_templates.xml`
- `dipl_doc_sale/i18n/es_AR.po`

### Contenido esperado por archivo

#### `__manifest__.py`

Debe definir:

- nombre del módulo,
- summary,
- versión inicial,
- dependencia `sale_management`,
- data files de reportes,
- `installable = True`.

#### `README.md`

Debe documentar:

- propósito del módulo,
- alcance actual de `V1`,
- política documental no fiscal,
- relación con futuras iteraciones.

#### `CHANGELOG.md`

Debe registrar:

- creación inicial del módulo,
- incorporación del reporte formal comercial,
- decisiones documentales relevantes de la `V1`.

#### `quote_report_actions.xml`

Debe declarar:

- la nueva `ir.actions.report`,
- vínculo con `sale.order`,
- nombre visible de la acción,
- template asociado.

#### `quote_report_templates.xml`

Debe contener:

- plantilla principal,
- snippets reutilizables,
- estilos necesarios para impresión.

## Seguridad

### Decisión

No se requieren nuevos grupos ni reglas de acceso en `V1`.

### Motivo

- el reporte se basa en `sale.order`,
- se apoya en permisos ya existentes del módulo de ventas,
- no introduce nuevos modelos.

## Integración con módulos existentes

### Con `dipl_sale_technical_quote`

No habrá dependencia directa en `V1`.

Si una orden usa datos técnicos de ese módulo, el nuevo reporte podrá seguir mostrando los datos visibles ya presentes en la orden, pero no debe asumir ownership de esa lógica.

### Con localización AR

Se tomará inspiración visual y estructural de:

- `l10n_ar.custom_header`
- `l10n_ar_sale`

Pero sin heredar la lógica tributaria ni depender del módulo como requisito.

## Riesgos de diseño

### 1. Riesgo de similitud excesiva con factura fiscal

Si el layout se parece demasiado a una factura A real, puede generar ambigüedad comercial o fiscal.

Mitigación:

- incluir leyenda no fiscal,
- no usar semántica de documento tributario válido,
- mantener título principal explícito: `Cotización`.

### 2. Riesgo de invasividad funcional

Si el nuevo reporte reemplaza demasiado pronto al estándar, cualquier error visual o funcional impactará el flujo actual.

Mitigación:

- en `V1`, usar acción nueva en lugar de sustitución del reporte estándar.

### 3. Riesgo de crecimiento desordenado

Si en implementación se intenta meter ya lista de corte u orden interna, se rompe el foco de la iteración.

Mitigación:

- mantener `V1` estrictamente limitada a la cotización formal comercial.

## Slice de implementación recomendado

### Slice 1

Scaffolding del módulo:

- estructura base,
- manifest,
- README,
- CHANGELOG,
- acción de reporte vacía o mínima.

### Slice 2

Plantilla principal de cotización:

- layout general,
- header,
- bloque cliente,
- metadata comercial.

### Slice 3

Tabla de líneas y bloque de totales:

- líneas,
- subtotales,
- impuestos,
- total.

### Slice 4

Refinamiento visual y documental:

- estilos de impresión,
- leyenda no fiscal,
- condiciones y notas,
- verificación final de legibilidad.

## Criterio de salida a Coding

El diseño puede considerarse listo para implementación si aceptamos estas decisiones:

- módulo nuevo `dipl_doc_sale`,
- dependencia mínima `sale_management`,
- `V1` solo cotización formal comercial,
- acción de reporte nueva,
- sin nuevos modelos ni campos persistentes,
- inspiración visual argentina sin semántica fiscal de factura,
- arquitectura QWeb modular con snippets compartidos.

## Próxima etapa

Coding

Resultado esperado:

- módulo scaffolded,
- acción de reporte creada,
- plantilla formal de cotización implementada,
- README y CHANGELOG alineados,
- primera versión funcional lista para validación visual.
