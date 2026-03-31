# Wizard Pattern — Dipleg Odoo 19

Complete Python template for a `TransientModel` (wizard). Copy and adapt for each new wizard.

## Wizard Model (`wizards/{name}_wizard.py`)

```python
# -*- coding: utf-8 -*-
from odoo import api, fields, models
from odoo.exceptions import UserError


class DiplExampleWizard(models.TransientModel):
    _name = "dipl.example.wizard"
    _description = "Example Wizard"

    # === FIELDS ===
    # Receive active records from context
    example_ids = fields.Many2many(
        "dipl.example.model",
        default=lambda self: self._default_example_ids(),
        string="Records",
    )
    date = fields.Date(default=fields.Date.context_today, required=True)
    note = fields.Text()

    # === DEFAULTS ===
    @api.model
    def _default_example_ids(self):
        active_ids = self.env.context.get("active_ids", [])
        return self.env["dipl.example.model"].browse(active_ids)

    # === ACTIONS ===
    def action_apply(self):
        self.ensure_one()
        if not self.example_ids:
            raise UserError("No records selected.")

        # Process records in batch
        self.example_ids.write({"state": "confirmed"})

        return {"type": "ir.actions.act_window_close"}
```

## Wizard View (`wizards/{name}_wizard_views.xml`)

```xml
<odoo>
    <record id="dipl_example_wizard_view_form" model="ir.ui.view">
        <field name="name">dipl.example.wizard.form</field>
        <field name="model">dipl.example.wizard</field>
        <field name="arch" type="xml">
            <form string="Example Wizard">
                <group>
                    <field name="example_ids" widget="many2many_tags"/>
                    <field name="date"/>
                    <field name="note"/>
                </group>
                <footer>
                    <button name="action_apply" type="object"
                            string="Apply" class="btn-primary"/>
                    <button string="Cancel" class="btn-secondary"
                            special="cancel"/>
                </footer>
            </form>
        </field>
    </record>

    <record id="dipl_example_wizard_action" model="ir.actions.act_window">
        <field name="name">Example Wizard</field>
        <field name="res_model">dipl.example.wizard</field>
        <field name="view_mode">form</field>
        <field name="target">new</field>
        <field name="binding_model_id" ref="dipl_example.model_dipl_example_model"/>
        <field name="binding_view_types">list,form</field>
    </record>
</odoo>
```

## ACL entry (`security/ir.model.access.csv`)

```csv
id,name,model_id:id,group_id:id,perm_read,perm_write,perm_create,perm_unlink
access_dipl_example_wizard_user,dipl.example.wizard user,model_dipl_example_wizard,base.group_user,1,1,1,1
```

## Key conventions

- `action_apply` must call `self.ensure_one()` first.
- Use `self.env.context.get("active_ids", [])` to receive records from list selection.
- Batch process via `.write({...})` on the recordset — never loop with individual writes.
- `target="new"` is mandatory for wizards — opens as a dialog.
- Always add an ACL entry even for transient models.
