# DIPL - Cotización por Peso y Minutos

Módulo profesional de Odoo para calcular precios de productos de corte/plegado de metal basándose en dimensiones físicas, peso y tiempo de proceso.

## Características

✅ **Cálculo Automático de Peso** - Calcula el peso basándose en volumen × densidad del material  
✅ **Precios Dinámicos** - Cálculo por kg y opcionalmente por minutos de corte  
✅ **Redondeo Automático** - Precios redondeados a miles para facilitar cotización  
✅ **Expresiones Matemáticas** - Soporta expresiones como `1100+50+50` en dimensiones  
✅ **Suite de Tests** - 40+ tests unitarios para garantizar calidad  
✅ **Logging Completo** - Sistema de logging para debugging y auditoría  

## Requisitos

- Odoo Community 19.0 o superior
- Python 3.10+
- Módulo `sale` instalado
- Biblioteca `simpleeval` (se instala automáticamente)

## Instalación

1. **Copiar el módulo**

   ```bash
   cp -r dipl_sale_pricing /path/to/odoo/addons/custom/
   ```

2. **Instalar dependencias Python**

   ```bash
   pip install -r requirements.txt
   ```

3. **Actualizar lista de aplicaciones**
   - Ir a Aplicaciones → Actualizar lista de aplicaciones

4. **Instalar módulo**
   - Buscar "DIPL - Cotización por Peso"
   - Click en Instalar

## Configuración

### 1. Crear Producto Personalizado

```
Ventas → Productos → Crear
```

- **Nombre**: Chapa de Acero 3mm
- **Tipo**: Almacenable
- **✓ ¿Es personalizado?**: Marcar
- **Tipo de Cálculo**: Solo por Kg (o Kg + Minutos)
- **Precio por Kg**: $5,000
- **Densidad**: 7.85 g/cm³ (acero)
- **Espesor**: 3 mm

### 2. Crear Orden de Venta

```
Ventas → Órdenes → Crear
```

- Seleccionar cliente
- Agregar línea:
  - **Producto**: Chapa de Acero 3mm
  - **Cantidad**: 10
  - **Desarrollo**: 1200 (o expresión: `1100+50+50`)
  - **Largo**: 2000
  - El peso y precio se calculan automáticamente

## Uso

### Expresiones Matemáticas

Los campos de dimensiones soportan expresiones:

```
1100+50+50        → 1200
2000-100          → 1900
(100+200)*4       → 1200
```

### Cálculo de Peso

Fórmula utilizada:

```
Volumen (mm³) = Desarrollo × Largo × Espesor
Volumen (cm³) = Volumen (mm³) / 1000
Peso (g) = Volumen (cm³) × Densidad (g/cm³)
Peso (kg) = Peso (g) / 1000
```

### Ejemplos de Materiales

| Material | Densidad (g/cm³) |
|----------|------------------|
| Acero | 7.85 |
| Acero Inoxidable | 8.00 |
| Aluminio | 2.70 |
| Cobre | 8.96 |
| Bronce | 8.73 |

## Testing

Ejecutar tests unitarios:

```bash
cd /path/to/odoo
python3 odoo-bin -c odoo.conf -d test_db \
  --test-enable --stop-after-init -u dipl_sale_pricing
```

## Soporte

- **Autor**: DIPLEG
- **Versión**: 19.0.2.0.0
- **Licencia**: LGPL-3

## Changelog

### Version 2.0.0 (2026-02-09)

- ✨ Suite completa de tests unitarios (40+ tests)
- ✨ Sistema de logging profesional
- ✨ Constantes nombradas para mejor mantenibilidad
- ✨ Mejor manejo de errores con mensajes específicos
- ✨ Documentación exhaustiva con docstrings
- 🔧 Preparado para migración a simpleeval
- 📝 README completo

### Version 1.1.0 (2026-01-30)

- ✨ Versión inicial funcional
- ✨ Cálculo por peso y minutos
- ✨ Redondeo a miles
- ✨ Evaluación de expresiones matemáticas
