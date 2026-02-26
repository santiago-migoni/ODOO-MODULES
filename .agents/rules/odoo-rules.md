---
trigger: always_on
glob: "*.py, *.xml, *.csv, __manifest__.py"
description: Reglas de desarrollo y arquitectura de módulos Odoo
---

# Reglas de Odoo

Basado en las mejores prácticas de la industria y la skill `odoo-development`.

## 1. Calidad de Código y Arquitectura

- **Convenciones**: Seguir estrictamente PEP-8 para Python y nombramiento descriptivo alineado a Odoo.
- **Modularidad**: Aprovechar siempre el ORM de Odoo, los decoradores (`@api.model`, `@api.depends`, etc.) y la herencia de vistas XML (`<xpath>`).
- **Separación de Responsabilidades**: Distinguir claramente entre modelos, vistas, controladores, datos y seguridad.

## 2. Implementación y Patrones

- **No modificar el Core**: Todo comportamiento debe alterarse mediante la herencia o extensión, jamás modificando el código fuente original.
- **Validaciones Rigurosas**: Emplear excepciones nativas (`ValidationError`, `UserError`) y restricciones (`@api.constrains`).
- **Seguridad primero**: Toda capa arquitectónica debe estar protegida. Definir explícitamente derechos en `ir.model.access.csv` y reglas de registro (record rules) en XML.

## 3. Internacionalización y Rendimiento

- **Traducciones**: Envolver siempre las cadenas literales con `_()` para hacerlas traducibles.
- **Optimización de ORM**: Emplear filtros eficientes en `domain` y `context`, hacer uso de `prefetch_fields` y delegar tareas muy pesadas a cron jobs o acciones programadas.

## 4. Estructura Obligatoria del Módulo

Todo módulo nuevo debe seguir el esquema de directorios estándar de Odoo:
`models/`, `views/`, `security/`, `data/`, `controllers/`, `static/`, `wizards/`, `reports/`.
