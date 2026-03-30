# -*- coding: utf-8 -*-
"""Plantilla de modelo Odoo estándar Dipleg.

Uso: copiar y adaptar para nuevos modelos en módulos dipl_*.
Sigue OCA coding standards y Odoo 19 API.
"""
from odoo import api, fields, models
from odoo.exceptions import ValidationError


class DiplExampleModel(models.Model):
    _name = "dipl.example.model"
    _description = "Example Model"
    _inherit = ["mail.thread", "mail.activity.mixin"]
    _order = "sequence, name"

    # === FIELDS ===#
    name = fields.Char(required=True, tracking=True)
    sequence = fields.Integer(default=10)
    active = fields.Boolean(default=True)
    company_id = fields.Many2one(
        "res.company",
        default=lambda self: self.env.company,
        required=True,
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

    # === Relational ===#
    partner_id = fields.Many2one("res.partner", string="Partner")
    line_ids = fields.One2many(
        "dipl.example.model.line", "parent_id", string="Lines"
    )
    tag_ids = fields.Many2many("dipl.example.tag", string="Tags")

    # === Computed ===#
    total = fields.Float(compute="_compute_total", store=True)

    # === COMPUTE ===#
    @api.depends("line_ids.amount")
    def _compute_total(self):
        for record in self:
            record.total = sum(record.line_ids.mapped("amount"))

    # === CONSTRAINTS ===#
    @api.constrains("name")
    def _check_name(self):
        for record in self:
            if record.name and len(record.name) < 3:
                raise ValidationError("Name must be at least 3 characters.")

    # === ACTIONS ===#
    def action_confirm(self):
        self.filtered(lambda r: r.state == "draft").write(
            {"state": "confirmed"}
        )

    def action_cancel(self):
        self.write({"state": "cancelled"})

    # === CRUD OVERRIDES ===#
    @api.model_create_multi
    def create(self, vals_list):
        # Add custom logic before create if needed
        return super().create(vals_list)
