---
trigger: always_on
glob:
description:
---

# Reglas de Desarrollo Odoo (.agent/rules/coding.md)

> Estas son las reglas **irrompibles** del proyecto. Definen el Tech Stack, el Style Guide y los estándares de calidad que siempre deben respetarse.

## 1. Estándares Generales

- **Base**: Guías de la OCA (Odoo Community Association), adaptadas al proyecto.
- **Idioma**: Comentarios, documentación y docstrings en **Español**.
- **Código Python**: Variables y métodos en inglés (estándar técnico), pero explicaciones en español.

## 2. Naming Conventions (Nombres)

- **Módulos Técnicos**: `dipl_[categoría]_[descripción]`
  - Ejemplo Ventas: `dipl_sale_reportes_avanzados`
  - Ejemplo Inventario: `dipl_stock_ajustes`
- **Clases/Modelos**:
  - `_name`: `dipl.[categoría].[modelo]` (e.g., `dipl.sale.order.line`).
  - `_inherit`: Usar el nombre original si es extensión directa.
- **Vistas XML**:
  - IDs: `view_[modelo]_[tipo]_[sufijo]` (e.g., `view_sale_order_form_dipl_filters`).
  - XPath: Usar atributos explícitos (`name`, `id`) para ubicar elementos.
  - **PROHIBIDO**: Evitar índices numéricos frágiles (`//field[3]`). Siempre preferir atributos técnicos.

## 3. Calidad de Código

- **Manifest**: Siempre definir `installable: True`. Dependencias deben ser exactas.
- **Versionado de Módulos**: Formato `[versión_odoo].[versión_módulo]` (ej: `19.0.1`). La versión de Odoo se toma del entorno actual. La versión del módulo es incremental.
- **Seguridad**: Todo modelo nuevo debe tener `ir.model.access.csv`.
- **Linting**: Respetar PEP8 (espacios, indentación).

## 4. Tests Automatizados (Estándar)

- **Política**: Cada nuevo módulo o funcionalidad crítica **debe** incluir tests.
- **Responsabilidad**: El Agente (yo) escribirá los tests unitarios y de tour para asegurar la calidad.
- **Ubicación**: Carpeta `tests/` dentro de cada módulo.
- **Ejecución**: Se deben pasar los tests antes de subir a Staging.

## 5. Documentación General

- **Aplicabilidad**: Todo documento markdown (`.md`), sea en `docs/` o raíz.
- **Estructura Obligatoria**:
  1. `# Título Principal`
  2. `## Índice` (Lista con enlaces a las secciones).
  3. `## Resumen Ejecutivo` (Máximo 100 palabras).
  4. `## Desarrollo` (Encabezados, párrafos, tablas, etc).
- **Nomenclatura (docs/)**:
  - Módulos: `dipl_[categoría]_[descripción].md` (ej. `dipl_sale_orders.md`).
  - General: `dipl_odoo_[description_in_english].md` (ej. `dipl_odoo_setup_guide.md`).
- **Consolidación**: Evitar documentos dispersos; agrupar por temática.

## 6. Gestión de Cambios (Changelog)

- **Timing**: Actualizar el `CHANGELOG.md` cada vez que se complete una funcionalidad (`feat`) o corrección (`fix`) relevante.
- **Sección**: Usar la sección `[Unreleased]` para cambios pendientes de lanzamiento.
- **Formato**: Seguir el estándar [Keep a Changelog](https://keepachangelog.com/es-ES/1.0.0/).
- **Commits vs Changelog**:
  - Los commits son técnicos y detallados.
  - El changelog es un resumen curado para humanos.
  - Al hacer un release (`staging` -> `main`), mover `[Unreleased]` a una nueva sección con versión y fecha.
