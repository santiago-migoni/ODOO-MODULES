# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [2.0.0] - 2026-02-09

### Added

- Suite completa de tests unitarios con 40+ test cases
  - `tests/test_expressions.py` - Tests de evaluación de expresiones y redondeo
  - `tests/test_product_template.py` - Tests de producto personalizado
  - `tests/test_sale_order_line.py` - Tests de cálculo de peso y precios
- Sistema de logging profesional en todos los módulos
- Constantes nombradas para mejor mantenibilidad:
  - `MM3_TO_CM3 = 1000` - Conversión mm³ a cm³
  - `G_TO_KG = 1000` - Conversión gramos a kilogramos
  - `ROUNDING_UNIT = 1000` - Unidad de redondeo
- Documentación exhaustiva con docstrings y ejemplos
- README.md completo con instrucciones de instalación y uso
- CHANGELOG.md para seguimiento de versiones
- requirements.txt con dependencias Python

### Changed

- Versión actualizada de `19.0.1.1.0` a `19.0.2.0.0`
- Mejora en manejo de errores con excepciones específicas
- Descripción del manifest mejorada con nuevas características
- Preparación para migración a simpleeval (TODO incluido en código)

### Fixed

- Mejor validación de expresiones inválidas con logging
- Mensajes de error más descriptivos

### Security

- Preparado para reemplazar `eval()` con `simpleeval` para mayor seguridad
- Validación robusta de entrada en expresiones matemáticas

## [1.1.0] - 2026-01-30

### Added

- Versión inicial funcional del módulo
- Cálculo automático de peso basado en dimensiones
- Dos modos de cálculo: solo kg, o kg + minutos
- Redondeo automático a miles
- Evaluación de expresiones matemáticas en dimensiones
- Integración con listas de precios y descuentos de Odoo
- Reportes PDF personalizados con dimensiones
- Vistas personalizadas en productos y órdenes de venta

### Changed

- N/A (primera versión)

### Deprecated

- N/A

### Removed

- N/A

### Fixed

- N/A

### Security

- Uso de `eval()` con `__builtins__` vacíos para evaluación de expresiones

## Formato

- **Added** - Nuevas características
- **Changed** - Cambios en funcionalidad existente
- **Deprecated** - Características que serán removidas
- **Removed** - Características removidas
- **Fixed** - Corrección de bugs
- **Security** - Vulnerabilidades corregidas o mejoras de seguridad
