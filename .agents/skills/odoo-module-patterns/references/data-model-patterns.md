# Data Model Patterns Guide

Standard patterns for Odoo 19 business objects.

## 1. State Machines

Always use `Selection` for model status:
- `draft`: New records, editable.
- `confirmed`: Validated, ready for processing.
- `done`: Finalized, read-only.
- `cancel`: Dismissed.

### Statusbar Widget
Use it in the header for visibility:
```xml
<header>
    <button name="action_confirm" type="object" string="Confirm" class="btn-primary" invisible="state != 'draft'"/>
    <field name="widget" widget="statusbar" statusbar_visible="draft,confirmed,done"/>
</header>
```

## 2. Parent-Child Relations (Lines)

For models with list details (e.g., Quotations, Sales Orders):
- **Header**: Main model (`One2many` to lines).
- **Line**: Detailed model (`Many2one` back to header).

**Tip**: Use `sequence` (integer) for sorting lines.

## 3. Multi-Company Support

Always include `company_id` for entities with financial impact:
```python
company_id = fields.Many2one(
    comodel_name="res.company",
    string="Company",
    default=lambda self: self.env.company,
    required=True,
    index=True,
)
```

## 4. Computed Fields & Performance

- **Store=True**: If the field is used in views/reports often.
- **Depends**: Correct dependency list is critical to avoid old data.
- **Recursive**: Avoid deep recursive computes that trigger re-re-computes.

## 5. Record Naming (`_rec_name`)

If the model doesn't have a `name` field, define `_rec_name` or override `_compute_display_name` (Odoo 17+ naming convention).
