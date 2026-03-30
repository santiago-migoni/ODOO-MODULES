---
description: Crea un wizard transaccional en un módulo de Odoo 19.
---
# Add Wizard Workflow

Process to create a `TransientModel` (wizard) in a custom Odoo 19 module.

The argument `$ARGUMENTS` contains the wizard name and module.

## 1. Context

1. Define the purpose: what records does the wizard process and what action does it perform?
2. Clarify the trigger: button on a form, action menu on a list, or top-level menu item?
3. If triggered from a list, confirm it needs `active_ids` from context.

## 2. Technical proposal

Present:
- `wizards/{wizard_name}.py` — `TransientModel` with fields and `action_apply`.
- `wizards/{wizard_name}_views.xml` — `<form>` view with `<footer>` buttons.
- `security/ir.model.access.csv` — entry for the transient model.
- Connection point to the main model (button action or menu action).

**WAIT FOR USER APPROVAL.**

## 3. Implementation

1. **Python**: Create the `TransientModel`. Method naming: `action_apply` for the primary action.
2. **View**: `<form>` with `<footer>` containing primary and cancel buttons:
    ```xml
    <footer>
        <button name="action_apply" type="object" string="Apply" class="btn-primary"/>
        <button string="Cancel" class="btn-secondary" special="cancel"/>
    </footer>
    ```
3. **Action**: `ir.actions.act_window` with `target="new"` and correct `res_model`.
4. **Context-aware**: If the wizard acts on selected records, read `self.env.context.get("active_ids", [])` inside `action_apply`.
5. **ACL**: Add entry to `ir.model.access.csv` (transient models still need it).

## 4. Verification

Use `/generate-tests` to generate a `TransactionCase` covering `action_apply` with valid and edge-case inputs.
