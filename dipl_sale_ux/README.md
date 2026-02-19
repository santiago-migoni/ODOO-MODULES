# DIPL - Filtro de Cotizaciones Activas

## Descripción

Módulo de mejora de UX para el módulo de ventas de Odoo que agrega un filtro predeterminado para mostrar solo cotizaciones activas (no vencidas).

## Características

- ✅ **Filtro predeterminado**: Al abrir la vista de cotizaciones, se muestra automáticamente solo las cotizaciones activas
- ✅ **Flexible**: Los usuarios pueden desactivar el filtro si necesitan ver todas las cotizaciones
- ✅ **Criterios claros**:
  - Estado: Borrador (`draft`) o Enviada (`sent`)
  - Fecha de validez: Mayor o igual a hoy, o sin fecha definida
- ✅ **No invasivo**: No modifica datos, solo cambia la vista predeterminada

## Instalación

1. Copiar el módulo a la carpeta `addons/custom/`
2. Actualizar la lista de módulos en Odoo
3. Instalar el módulo "DIPL - Filtro de Cotizaciones Activas"

## Uso

Una vez instalado:

1. Ve a **Ventas > Órdenes > Cotizaciones**
2. Por defecto verás solo las cotizaciones activas (filtro activado automáticamente)
3. Para ver todas las cotizaciones, desactiva el filtro "Cotizaciones Activas" en la barra de búsqueda

## Criterios del Filtro

El filtro "Cotizaciones Activas" muestra órdenes de venta que cumplan:

```python
[
    ('state', 'in', ['draft', 'sent']),  # Solo borradores o enviadas
    '|',                                  # O
    ('validity_date', '>=', hoy),        # Fecha de validez >= hoy
    ('validity_date', '=', False)        # O sin fecha de validez
]
```

## Dependencias

- `sale`: Módulo de ventas de Odoo

## Versión

- **Versión del módulo**: 1.0.0
- **Compatibilidad**: Odoo 19.0

## Autor

DIPLEG

## Licencia

LGPL-3
