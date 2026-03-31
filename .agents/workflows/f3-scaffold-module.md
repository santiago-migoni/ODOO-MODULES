---
description: Crea un nuevo módulo de Odoo 19 siguiendo las convenciones de Dipleg.
---
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
