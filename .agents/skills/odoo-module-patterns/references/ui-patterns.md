# UI Patterns Guide

Best practices and code patterns for Odoo 19 User Interface design.

## 1. Wizards (TransientModels)

TransientModels handle short-lived user interaction. Footer structure is mandatory:

```xml
<form string="Wizard Title">
    <group>
        <field name="field_one"/>
        <field name="field_two"/>
    </group>
    <footer>
        <button name="action_apply" type="object" string="Apply" class="btn-primary"/>
        <button string="Cancel" class="btn-secondary" special="cancel"/>
    </footer>
</form>
```

Action definition: always `target="new"`, binding via `binding_model_id` or a button on the parent form.

## 2. Smart Buttons

For displaying related record counts and navigating from a parent record:

```xml
<!-- In the form view, inside <div class="oe_button_box" name="button_box"> -->
<button type="object" name="action_open_related"
        class="oe_stat_button" icon="fa-file-text-o"
        invisible="related_count == 0">
    <field name="related_count" widget="statinfo" string="Related"/>
</button>
```

Computed field for the count:
```python
related_count = fields.Integer(compute="_compute_related_count")

def _compute_related_count(self):
    for record in self:
        record.related_count = self.env["related.model"].search_count(
            [("parent_id", "=", record.id)]
        )
```

## 3. Chatter (Mail Thread)

For all main business objects — enables messages, activity scheduling, and follower tracking:

```xml
<chatter/>
```

Requires the model to inherit `mail.thread`:
```python
class DiplExample(models.Model):
    _name = "dipl.example"
    _inherit = ["mail.thread", "mail.activity.mixin"]
```

## 4. Status Bar

For models with a state machine, always display in the form header:

```xml
<header>
    <button name="action_confirm" type="object" string="Confirm"
            class="btn-primary" invisible="state != 'draft'"/>
    <field name="state" widget="statusbar" statusbar_visible="draft,confirmed,done"/>
</header>
```

## 5. Search View — Portal & Mobile

- **Filters**: always add `My Records` (`user_id = uid`) and common state filters.
- **Group By**: always add `Company` and `Creation Date` as defaults.
- **Portal users**: use `invisible` conditions with `groups` attribute to hide internal fields, not a separate view.
