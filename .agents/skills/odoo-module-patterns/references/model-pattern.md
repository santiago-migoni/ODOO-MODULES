# Model Pattern — Dipleg Odoo 19

Complete Python template for a new `dipl_*` model. Copy and adapt for each new module.

## Base Model (`models/{name}.py`)

```python
# -*- coding: utf-8 -*-
from odoo import api, fields, models
from odoo.exceptions import ValidationError


class DiplExampleModel(models.Model):
    _name = "dipl.example.model"
    _description = "Example Model"
    _inherit = ["mail.thread", "mail.activity.mixin"]
    _order = "sequence, name"

    # === FIELDS ===
    name = fields.Char(required=True, tracking=True)
    sequence = fields.Integer(default=10)
    active = fields.Boolean(default=True)
    company_id = fields.Many2one(
        "res.company",
        default=lambda self: self.env.company,
        required=True,
        index=True,
    )
    state = fields.Selection(
        [
            ("draft", "Draft"),
            ("confirmed", "Confirmed"),
            ("done", "Done"),
            ("cancelled", "Cancelled"),
        ],
        default="draft",
        tracking=True,
    )

    # === RELATIONAL ===
    partner_id = fields.Many2one("res.partner", string="Partner", index=True)
    line_ids = fields.One2many("dipl.example.model.line", "parent_id", string="Lines")
    tag_ids = fields.Many2many("dipl.example.tag", string="Tags")

    # === COMPUTED ===
    total = fields.Float(compute="_compute_total", store=True)

    # === COMPUTE ===
    @api.depends("line_ids.amount")
    def _compute_total(self):
        for record in self:
            record.total = sum(record.line_ids.mapped("amount"))

    # === CONSTRAINTS ===
    @api.constrains("name")
    def _check_name(self):
        for record in self:
            if record.name and len(record.name) < 3:
                raise ValidationError("Name must be at least 3 characters.")

    # === ACTIONS ===
    def action_confirm(self):
        self.filtered(lambda r: r.state == "draft").write({"state": "confirmed"})

    def action_cancel(self):
        self.write({"state": "cancelled"})

    # === CRUD OVERRIDES ===
    @api.model_create_multi
    def create(self, vals_list):
        return super().create(vals_list)
```

## Key conventions

- Always use `@api.model_create_multi` (never `create(self, vals)` in Odoo 19).
- Actions must handle **recordsets** — use `self.filtered()` or `self.write()`.
- Computed fields that appear in list views must have `store=True`.
- `company_id` is required for any model with financial impact.
- `_order` should always be explicit — never rely on insertion order.
