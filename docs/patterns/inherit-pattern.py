# -*- coding: utf-8 -*-
"""Plantilla de herencia de modelo Odoo estándar Dipleg.

Uso: copiar y adaptar cuando se necesita extender un modelo existente
de Odoo (res.partner, sale.order, etc.) con campos o lógica custom.
"""
from odoo import api, fields, models


class ResPartnerInherit(models.Model):
    """Extensión de res.partner con campos custom Dipleg."""

    _inherit = "res.partner"
    # NO definir _name — se extiende el modelo original

    # === CAMPOS CUSTOM ===#
    # Prefijo x_ no es obligatorio pero ayuda a identificar campos custom
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

    # === COMPUTED ===#
    dipl_order_count = fields.Integer(
        compute="_compute_dipl_order_count",
        string="Order Count",
    )

    def _compute_dipl_order_count(self):
        # Evitar N+1: una sola query con read_group
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

    # === OVERRIDE DE MÉTODO ===#
    def _get_name(self):
        """Agregar categoría al nombre mostrado."""
        name = super()._get_name()
        if self.dipl_category and self.dipl_category != "standard":
            name = f"[{self.dipl_category.upper()}] {name}"
        return name
