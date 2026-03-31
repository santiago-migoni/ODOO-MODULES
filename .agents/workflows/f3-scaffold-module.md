---
description: Crea un nuevo módulo de Odoo 19 siguiendo las convenciones de Dipleg.
---

> **Fase**: F3 — Diseño Arquitectónico
> **Dónde estamos**: El análisis ha mapeado el código existente. Creamos la estructura base del módulo.
> **Por qué esta fase**: La estructura de directorios de Odoo no es preferencia estilística — es ingeniería que permite al framework localizar recursos e inyectarlos en el registro central.
> **Habilita**: Fase 4 (Implementación) — produce el esqueleto donde los desarrolladores codificarán modelos, vistas y lógica.

# Scaffold Module Workflow

Create a new Odoo 19 module for Dipleg following repository conventions.

The argument `$ARGUMENTS` contains the module name (without the `dipl_` prefix). If not provided, ask for it.

## 1. Pre-flight questions (ask once, consolidated)

Before generating any file, confirm:
- **Module name** (if not in `$ARGUMENTS`).
- **Short description** (summary field in manifest).
- **Optional features** — answer yes/no for each:
    - Multi-company support? (`company_id` + record rule)
    - OWL frontend components? (`static/src/` + assets in manifest)
    - Reports? (`report/` folder + action)
    - Wizards? (`wizards/` folder)

## 2. Base structure (always generated)

```
dipl_{name}/
├── __init__.py
├── __manifest__.py
├── CHANGELOG.md
├── models/
│   ├── __init__.py
│   └── {name}.py
├── views/
│   ├── {name}_views.xml
│   └── menus.xml
├── security/
│   ├── ir.model.access.csv
│   └── security.xml          # always: at least one group
├── tests/
│   ├── __init__.py
│   └── test_{name}.py
└── i18n/
    └── es.po
```

Optional additions based on answers:
- `static/src/` — if OWL selected.
- `report/` — if Reports selected.
- `wizards/` — if Wizards selected.

## 3. Manifest template

Generate the manifest including only what was confirmed:

```python
{
    "name": "Dipleg - {Display Name}",
    "version": "19.0.1.0.0",
    "category": "{Category}",
    "summary": "{Short Description}",
    "author": "Dipleg",
    "website": "https://dipleg.com",
    "license": "LGPL-3",
    "depends": ["base", "mail"],
    "data": [
        "security/security.xml",
        "security/ir.model.access.csv",
        "views/{name}_views.xml",
        "views/menus.xml",
    ],
    # Include only if OWL was confirmed:
    # "assets": {
    #     "web.assets_backend": [
    #         "dipl_{name}/static/src/...",
    #     ],
    # },
    "installable": True,
    "application": False,
}
```

## 4. Multi-company (if confirmed)

Add to the main model:
```python
company_id = fields.Many2one(
    "res.company",
    string="Company",
    default=lambda self: self.env.company,
    required=True,
    index=True,
)
```

Add to `security/security.xml` a rule restricting records to `company_id` in `env.companies`.

## 5. Post-generation steps

1. Run `/translate` to populate `i18n/es.po` with all generated strings.
2. Run `/generate-tests` to cover the base model logic.
3. Install locally: `python odoo-bin -i dipl_{name} -d <db>`.

## Edge cases

- **OCA dependency**: If the module depends on an OCA addon, add it as a git submodule first (see `odoo-sh` skill §7) before adding to `depends`.
- **Existing similar module**: Always `grep -r "dipl_{name}"` in the repo before creating to avoid duplication.

## Decisión de Herencia (obligatoria antes de generar)

Antes de ejecutar el scaffold, confirmar el paradigma de herencia:

| Pregunta | Si la respuesta es... | Usar |
|---|---|---|
| ¿Estás agregando campos/comportamiento a un modelo existente? | Sí | Extension (`_inherit` sin `_name`) |
| ¿Necesitas una nueva entidad con identidad propia pero similar al padre? | Sí | Classical (`_name` + `_inherit`) |
| ¿Necesitas acceder a campos del padre sin duplicar datos? | Sí | Delegation (`_inherits`) |
| ¿Es un modelo completamente nuevo sin relación con modelos existentes? | Sí | Nuevo `models.Model` con `_name` único |

Ver rule `06-inheritance-strategy` para detalles completos.
