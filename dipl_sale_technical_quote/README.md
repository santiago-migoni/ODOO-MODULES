# Technical Sales Quotation

Modulo custom para Odoo 19 que agrega cotizacion tecnica industrial sobre `sale.order.line`.

El modulo esta orientado al flujo actual de Dipleg:
- productos tecnicos configurados con espesor, densidad y precio por kilogramo,
- lineas de venta tecnicas calculadas por `Flat Pattern` + `Flat Length`,
- `Technical Kilograms` siempre calculado,
- integracion con `price_unit`, impuestos y pricelists nativas de Odoo.

## Estado funcional actual

La politica vigente del modulo es `geometry-only`.

Eso significa:
- la linea tecnica calcula kilos solo por geometria,
- `Technical Kilograms` es readonly,
- no existe modo manual por kilos,
- si falta una o ambas medidas, la linea queda incompleta con kilos y precio en `0`.

## Dependencias

- `sale_management`

No declara dependencias Python adicionales fuera de la imagen base de Odoo 19.

## Campos principales

### Producto tecnico

En `product.template` el modulo agrega:
- `Technical Quote Product`
- `Thickness`
- `Density`
- `Theoretical Kilograms`

Reglas:
- si el producto es tecnico, `Thickness` debe ser mayor a `0`,
- `Density` debe ser mayor a `0`,
- `Sales Price` (`list_price`) se usa como precio maestro por kilogramo.

### Linea de venta tecnica

En `sale.order.line` el modulo usa:
- `Flat Pattern`
- `Flat Length`
- `Technical Kilograms`
- `Technical Price`

Campos internos de snapshot:
- `dipl_thickness_mm`
- `dipl_material_density`
- `dipl_price_per_kg`

Esos campos quedan ocultos del flujo normal de ventas y se usan para preservar el historico tecnico de la linea.

## Comportamiento funcional

### 1. Snapshot tecnico

Cuando una linea toma un producto tecnico, el modulo copia a la linea:
- espesor,
- densidad,
- precio por kilogramo.

Ese snapshot:
- no se resincroniza automaticamente si luego cambia la ficha del producto,
- se protege frente a payloads parciales de la vista inline,
- puede rehidratarse desde el producto si queda inconsistente.

### 2. Calculo tecnico

Si la linea es tecnica y tiene ambas medidas:
- `Flat Pattern > 0`
- `Flat Length > 0`

entonces calcula:
- `Technical Kilograms`
- `Technical Total`
- `Technical Unit Price`

Si falta una o ambas medidas:
- la linea queda `incomplete`,
- `Technical Kilograms = 0`,
- `Technical Price = 0`,
- `price_unit = 0`.

### 3. Pricing comercial

El modulo puentea el calculo tecnico a `price_unit` para que Odoo siga resolviendo:
- subtotal,
- impuestos,
- descuentos,
- reglas de pricelist.

Contrato actual:
- reglas `percentage` y `formula` pueden ajustar la base tecnica,
- reglas `fixed` se ignoran para lineas tecnicas,
- `Update Prices` es la accion explicita para recomputar precio comercial,
- un `Unit Price` manual deja de prevalecer si cambia una variable tecnica.

## Uso operativo

### Configuracion del producto

1. Ir a `Productos`.
2. Activar `Technical Quote Product`.
3. Cargar `Thickness`.
4. Cargar `Density`.
5. Definir `Sales Price` como precio por kilogramo.

### Cotizacion tecnica

1. Crear cotizacion en Ventas.
2. Agregar producto tecnico.
3. Definir `Quantity`.
4. Cargar `Flat Pattern`.
5. Cargar `Flat Length`.
6. Verificar:
   - `Technical Kilograms`
   - `Technical Price`
   - `Precio unitario`

## Vistas incluidas

- `views/product_template_views.xml`
- `views/sale_order_views.xml`
- `views/sale_order_line_views.xml`

La UI operativa queda reducida al set minimo visible para ventas.

## Tests

El modulo incluye cobertura automatizada en:
- `tests/test_module_install.py`
- `tests/test_sale_order_line_snapshot.py`

Los tests cubren:
- instalacion de campos,
- snapshot tecnico,
- lineas completas e incompletas,
- cambio de producto,
- proteccion de snapshot,
- `Update Prices`,
- regresion sobre lineas no tecnicas.

## Limitaciones conocidas

- La validacion automatizada local completa con `odoo-bin` depende de contar con un runtime Odoo 19 operativo en la maquina.
- El path legacy de `product.template.init()` debe seguir considerandose en validaciones de upgrade.
- La politica actual no contempla kilos manuales; cualquier necesidad futura de ese tipo requiere una decision funcional nueva.

## Archivos relevantes

- [__manifest__.py](/Users/santiago_migoni/Documents/Codex/quotation/dipl_sale_technical_quote/__manifest__.py)
- [CHANGELOG.md](/Users/santiago_migoni/Documents/Codex/quotation/dipl_sale_technical_quote/CHANGELOG.md)
- [product_template.py](/Users/santiago_migoni/Documents/Codex/quotation/dipl_sale_technical_quote/models/product_template.py)
- [sale_order_line.py](/Users/santiago_migoni/Documents/Codex/quotation/dipl_sale_technical_quote/models/sale_order_line.py)
