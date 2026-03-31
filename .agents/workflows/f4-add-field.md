---
description: Agrega un campo a un modelo existente en Odoo 19 con todas sus dependencias.
---
# Add Field Workflow

Focused process to add one or more fields to an existing Odoo 19 model.

The argument `$ARGUMENTS` contains the field name(s), type, and target module.

## 1. Context

1. Identify the target model file (`models/*.py`).
2. Determine:
    - Field type (`Char`, `Selection`, `Many2one`, `Float`, `Boolean`, etc.).
    - Stored (`store=True`) or computed (`compute=`).
    - If computed: list of `@api.depends` dependencies.
    - If `Many2one`: target comodel and whether it needs `index=True`.
3. Identify which views need updating (form, list, search).
4. If `store=True` and the module is already installed in production: **a migration script is required**.

## 2. Technical proposal

Present:
- Python field definition.
- Target view XML positions (before/after which existing field).
- Migration script path (if applicable).

**WAIT FOR USER APPROVAL.**

## 3. Implementation

1. **Python**: Add field to the model class. Respect field ordering conventions (group by functional area).
2. **Views**: Update `views/{model}_views.xml` using `<xpath>` position if inheriting, direct placement if in the module's own view.
3. **ACL**: If field is restricted to a group, add `groups="module.group_name"` to the field definition and the view widget.
4. **Migration** (if `store=True` and module is already installed):

    ```python
    # migrations/19.0.{next_version}/post-migration.py
    def migrate(cr, version):
        """Initialize new field {field_name} on {model_name}."""
        cr.execute("""
            UPDATE {table_name}
            SET {field_name} = {default_value}
            WHERE {field_name} IS NULL
        """)
    ```

    Replace `{table_name}` with the model's DB table name (`dipl_model_name` → `dipl_model_name`).

5. **i18n**: Add the field label and help string to `i18n/es.po` via `/translate`.

## 4. Quality gate

1. If computed: run `/generate-tests` to cover the compute logic.
2. Verify no `attrs=` used in XML (use `invisible=` directly).
3. If migration added: test the upgrade locally with `odoo-bin -u {module} -d {db}`.

## Edge cases

- **Name conflict with inherited model**: If the field name already exists in a `_inherit` parent, use a prefixed name (`dipl_{field_name}`) or override via `_compute` to add logic.
- **Removing a `store=True` field later**: Requires a migration to drop the DB column. Never just delete the field definition without a migration.
