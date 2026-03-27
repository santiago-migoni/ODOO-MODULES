---
trigger:
globs: "modules/**/i18n/**"
description: Translation standard (i18n/es.po, no en.po)
---

# translation-standard

Translation standard for custom Odoo modules:

- Base msgid/source strings are English (the strings you write).
- Translation output must be: `i18n/es.po`.
- Do not generate `i18n/en.po`.
- If more languages are requested, generate additional `i18n/<lang>.po` files.
