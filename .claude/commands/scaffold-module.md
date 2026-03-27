---
description: Crea un nuevo módulo de Odoo 19 siguiendo las convenciones de Dipleg.
---
Create a new Odoo 19 module for Dipleg following the repository conventions.


## Instructions
1. **Ask module name**: If not provided, ask for the module name (without the `dipl_` prefix).
2. **Verify duplicates**: Search in the repository for anything similar before creating.
3. **Consult patterns**: Review existing modules for established patterns.

## Structure to generate

```
dipl_{nombre}/
├── __init__.py
├── __manifest__.py
├── models/
│   ├── __init__.py
│   └── {nombre}.py            # Main model
├── views/
│   └── {nombre}_views.xml     # Form/List/Search views + menuitem
├── security/
│   ├── ir.model.access.csv    # Basic ACLs
│   └── security.xml           # Groups (if applicable)
├── tests/
│   ├── __init__.py
│   └── test_{nombre}.py       # Basic tests
├── data/                       # Only if initial data is needed
├── i18n/
│   └── es.po                  # Spanish translations (msgid base is English)
└── static/
    └── description/
        └── icon.png            # Placeholder icon
```

## Mandatory conventions
- **Technical name**: `dipl_{nombre}` (always with prefix)
- **Version**: `19.0.1.0.0`
- **License**: `LGPL-3`
- **Author**: `Dipleg`
- **Website**: `https://dipleg.com`
- **Category**: Ask the user
- **Dependencies**: Minimal (`base` always; add as needed)

## Manifest template

```python
{
    "name": "Dipleg - {Display Name}",
    "version": "19.0.1.0.0",
    "category": "{Category}",
    "summary": "{Short Summary}",
    "author": "Dipleg",
    "website": "https://dipleg.com",
    "license": "LGPL-3",
    "depends": ["base"],
    "data": [
        "security/ir.model.access.csv",
        "views/{nombre}_views.xml",
    ],
    "installable": True,
    "application": False,
}
```

## `i18n/es.po` template

Create `i18n/es.po` with the following minimal skeleton (no `i18n/en.po`):

```po
# Spanish translations for Dipleg custom module
# Module: dipl_{nombre}
msgid ""
msgstr ""
"Project-Id-Version: 19.0\n"
"Report-Msgid-Bugs-To: \n"
"POT-Creation-Date: \n"
"PO-Revision-Date: \n"
"Last-Translator: \n"
"Language-Team: Spanish\n"
"Language: es\n"
"MIME-Version: 1.0\n"
"Content-Type: text/plain; charset=UTF-8\n"
"Content-Transfer-Encoding: 8bit\n"
"Plural-Forms: nplurals=2; plural=(n != 1);\n"

# No translation entries by default.
# After generating models/views/XML strings, run Odoo translation export/import
# to populate msgid/msgstr pairs.
```

## At the end
- Show the tree of created files.
- Tell how to install: `odoo-bin -i dipl_{nombre}` (or via Apps in Odoo).
