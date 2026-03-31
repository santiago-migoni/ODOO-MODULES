---
name: odoo-module-patterns
description: >-
  Architectural decision guides for Odoo modules: when to extend vs create,
  ERD, technical decisions, and common design patterns. Use when planning
  new features or modules.
---

> **Fase**: F3 — Diseño Arquitectónico
> **Dónde estamos**: El análisis ha mapeado el código existente. Ahora diseñamos la arquitectura del módulo: herencia, modelos de datos, patrones de UI.
> **Qué hacer**: Decidir tipo de herencia, diseñar esquema de datos, seleccionar patrones de UI, definir estructura de directorios.
> **Cómo hacerlo**: Skill f3-module-patterns + workflows /scaffold-module, /new-feature.
> **Por qué así**: Una decisión de herencia incorrecta tiene implicaciones irreversibles en el rendimiento de la BD y puede costar decenas de miles de dólares en refactorización. Esta fase previene eso.

# Odoo Module Patterns - Master Index

Architectural guidance for Odoo 19 module design. Read the relevant reference before proposing any model or structure change.

## Decision Guides

| Topic | File | When to Use |
|---|---|---|
| Inheritance | `references/extend-vs-create.md` | Choosing between `_inherit`, `_inherits`, mixin, or new model |
| Dependencies | `references/module-dependencies.md` | Managing relations between custom / standard modules |
| Data Models | `references/data-model-patterns.md` | State machines, parent-child lines, multi-company fields |
| UI Patterns | `references/ui-patterns.md` | Wizards, smart buttons, chatter, search customization |
| Performance | `references/performance-patterns.md` | N+1 prevention, stored compute decisions, bulk ops |

## Code Templates (copy & adapt)

| Template | File | Use for |
|---|---|---|
| New Model | `references/model-pattern.md` | Base model with fields, compute, constraints, actions |
| Model Inheritance | `references/inherit-pattern.md` | Extending standard Odoo models (`res.partner`, etc.) |
| Wizard | `references/wizard-pattern.md` | TransientModel + form view + ACL entry |
| Views (XML) | `references/view-pattern.md` | Form, list, search, action and menuitem |
| Tests | `references/test-pattern.md` | TransactionCase with setUpClass and coverage priorities |
| Controller | `references/controller-pattern.md` | HTTP/JSON endpoints and file download routes |


## How to use these guides

1. **Start with `extend-vs-create.md`** when designing a new feature — it determines the structural approach before any code is written.
2. **Combine guides when needed**: a new model that has a wizard UI requires both `data-model-patterns` and `ui-patterns`.
3. **Reference `performance-patterns.md` on every model** with computed fields or search-heavy usage.
4. When none of the standard patterns fit, escalate: describe the situation and ask before inventing a new pattern.

## Core Principles (Dipleg)

- **Minimalism**: No field, method, or view unless it solves a real business need.
- **Traceability**: Use `mail.thread` + `mail.activity.mixin` for all main business objects.
- **Multi-company by default**: Include `company_id` if the model has any financial or inventory impact.
- **Batch-first**: Every Python method must handle a recordset of N records, not just one.

> For module folder structure and scaffolding, use `/scaffold-module`.

## Paradigma de Herencia — Decisión Obligatoria

Antes de codificar cualquier modelo, se DEBE elegir el paradigma de herencia correcto. Ver rule `06-inheritance-strategy` para la tabla completa de decisión.

Resumen rápido:
- **Extension** (`_inherit` sin `_name`): Tabla única. Para agregar campos/comportamiento a modelos existentes. Patrón más común.
- **Classical** (`_name` + `_inherit`): Tabla nueva con copia de columnas. Solo cuando la nueva entidad necesita identidad independiente.
- **Delegation** (`_inherits` + `Many2one`): Tablas enlazadas por FK. Para normalización sin duplicación de datos (patrón res.users → res.partner).

## Campos Polimórficos (fields.Reference)

Para flujos donde un registro debe vincularse a múltiples tipos de modelo (ej: actividad de seguimiento → factura O orden de compra O ticket):
- Usar `fields.Reference` con `selection` vía lambda para opciones dinámicas.
- Odoo almacena como cadena concatenada evaluable en la BD.
- Evita la proliferación de campos Many2one redundantes.

## Many2many con Metadatos

Cuando una relación Many2many requiere información adicional (fecha de asignación, estado, comentarios):
- Definir explícitamente la tabla intermedia (`rel`, `column1`, `column2`).
- O materializar como `models.Model` completo para inyectar campos adicionales.
