# Inherit Pattern — Dipleg Odoo 19

Template for extending standard Odoo models (`res.partner`, `sale.order`, etc.) with custom fields and logic.

## Extending a Standard Model (`models/{standard_model}_inherit.py`)

```python
# -*- coding: utf-8 -*-
from odoo import api, fields, models


class ResPartnerInherit(models.Model):
    """Dipleg extension of res.partner."""

    _inherit = "res.partner"
    # Do NOT define _name — extends the original model's table

    # === CUSTOM FIELDS ===
    # Prefix custom fields with dipl_ to identify ownership
    dipl_custom_field = fields.Char(string="Custom Field")
    dipl_category = fields.Selection(
        [
            ("standard", "Standard"),
            ("premium", "Premium"),
            ("vip", "VIP"),
        ],
        string="Category",
        default="standard",
    )
    dipl_credit_limit = fields.Monetary(
        string="Credit Limit",
        currency_field="currency_id",
    )
    dipl_notes = fields.Text(string="Internal Notes")

    # === COMPUTED (N+1 safe) ===
    dipl_order_count = fields.Integer(
        compute="_compute_dipl_order_count",
        string="Order Count",
    )

    def _compute_dipl_order_count(self):
        # Single query with read_group — never search() inside loop
        order_data = self.env["sale.order"].read_group(
            domain=[("partner_id", "in", self.ids)],
            fields=["partner_id"],
            groupby=["partner_id"],
        )
        mapped_data = {
            item["partner_id"][0]: item["partner_id_count"]
            for item in order_data
        }
        for partner in self:
            partner.dipl_order_count = mapped_data.get(partner.id, 0)

    # === METHOD OVERRIDE ===
    def _get_name(self):
        """Add category badge to display name."""
        name = super()._get_name()
        if self.dipl_category and self.dipl_category != "standard":
            name = f"[{self.dipl_category.upper()}] {name}"
        return name
```

## Key conventions

- **Never define `_name`** when using `_inherit` on a standard model — you'd create a new model instead of extending.
- **Always prefix custom fields** with `dipl_` to avoid collision with future Odoo updates.
- **Always call `super()`** in method overrides unless intentionally replacing behavior.
- Use `read_group()` for computed counts — never `search_count()` inside a loop.
- Add `depends` to your computed field if overriding it from a standard model.
