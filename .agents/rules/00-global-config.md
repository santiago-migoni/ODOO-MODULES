---
trigger: always_on
globs:
description: Configuración general y flujo de trabajo de Dipleg (Odoo 19, traducciones, ramas)
---
# Configuración del Repositorio - ODOO-MODULES

## Core
- **Odoo Version**: 19.0.x.y.z
- **License**: LGPL-3
- **Author**: Dipleg
- **Workflow**: `feature_branch_workflow`. Todas las tareas se realizarán en ramas específicas de funcionalidad.
- **Language**: Responder y proponer en **Español**. Toda la codificación y desarrollo de módulos será en **Inglés**. Comentarios en el código deben ser mínimos y en Inglés, solo si aportan valor.

## Colaboración y Proceso
- **Estrategia Propose-First**: No se deben realizar cambios directos en el código (Python, XML, etc.) sin proponer primero la estrategia.
  - Explicar el enfoque técnico.
  - Listar los archivos afectados.
  - Definir la estrategia de pruebas.
- **Minimal edits**: No refactorizar código sin relación.
- **No fallbacks**: Resolver la causa raíz del problema con un único camino en el código.
- **Calidad**: Mantener el código siguiendo los estándares de Odoo 19 (Checklist técnica).

## Internacionalización y Traducciones
- **Idioma Base**: English (en_US)
- **Idiomas de Destino**: Spanish (es_ES)
- **Estándar**:
  - Usar archivos de traducción `.po` (gettext).
  - No generar archivos `.po` para el idioma base (`en_US`).
  - Asegurar que los `msgid` sean exactos a los del código fuente.

## Contexto
- En caso de falta de contexto crítico o dudas sobre convenciones, usar la Skill de Odoo 19 o preguntar siempre antes de asumir.
