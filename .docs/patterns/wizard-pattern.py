# -*- coding: utf-8 -*-
"""Plantilla de wizard (TransientModel) estándar Dipleg.

Uso: copiar y adaptar para wizards en módulos dipl_*.
Los wizards son modelos temporales para acciones del usuario.
"""
from odoo import api, fields, models
from odoo.exceptions import UserError


class DiplExampleWizard(models.TransientModel):
    _name = "dipl.example.wizard"
    _description = "Example Wizard"

    # === FIELDS ===#
    # Contexto: recibir registros activos
    example_ids = fields.Many2many(
        "dipl.example.model",
        default=lambda self: self._default_example_ids(),
        string="Records",
    )
    date = fields.Date(default=fields.Date.context_today, required=True)
    note = fields.Text()

    # === DEFAULTS ===#
    @api.model
    def _default_example_ids(self):
        active_ids = self.env.context.get("active_ids", [])
        return self.env["dipl.example.model"].browse(active_ids)

    # === ACTIONS ===#
    def action_apply(self):
        self.ensure_one()
        if not self.example_ids:
            raise UserError("No records selected.")

        # Procesar registros
        for record in self.example_ids:
            record.write({"state": "confirmed"})

        # Retornar acción (cerrar wizard o abrir vista)
        return {"type": "ir.actions.act_window_close"}
