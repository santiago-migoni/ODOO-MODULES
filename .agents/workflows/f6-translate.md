---
description: Genera o actualiza traducciones es.po en un módulo de Odoo 19.
---
# Translate Workflow

Process to synchronize and update Odoo 19 Spanish translations (`es.po`).

The argument `$ARGUMENTS` contains the target module name.

## 1. Source scanning

Scan **all** these locations for translatable strings:

| Source | What to look for |
|---|---|
| `models/*.py` | `string=`, `help=`, `Selection` value labels, `ValidationError("...")` messages |
| `views/*.xml` | `string=` on fields/buttons/labels, `placeholder=`, `confirm=` on buttons |
| `wizards/*.py` / `wizards/*.xml` | Same as models and views |
| `report/*.xml` | Static text nodes inside QWeb templates |
| `data/*.xml` | `name` fields of records if they are user-facing |

Do **not** scan `tests/` — test code is never translated.

## 2. Generate / Update `i18n/es.po`

1. If `i18n/es.po` does not exist, create it with the standard PO header:

```po
# Spanish translations for Dipleg custom module
# Module: dipl_{name}
msgid ""
msgstr ""
"Project-Id-Version: 19.0\n"
"Language: es\n"
"MIME-Version: 1.0\n"
"Content-Type: text/plain; charset=UTF-8\n"
"Content-Transfer-Encoding: 8bit\n"
"Plural-Forms: nplurals=2; plural=(n != 1);\n"
```

2. For each discovered string, add an entry:
```po
msgid "Exact source string"
msgstr "Traducción al español"
```

3. `msgid` must match the source **exactly** — same capitalization, same punctuation.

## 3. Standards (Dipleg)

- Source language: **English** (`en_US`). All `msgid` are English.
- Target: **Spanish** (`es_ES`). Output file: `i18n/es.po` only.
- Do NOT generate `i18n/en.po`.
- For a new language beyond Spanish, generate `i18n/{lang_code}.po` following the same process.

## 4. Verification

1. Check for unescaped quotes inside `msgstr` (use `\"` not `"`).
2. Verify PO header is present and complete.
3. Do not modify existing `msgstr` entries unless the user explicitly requests a translation review.
