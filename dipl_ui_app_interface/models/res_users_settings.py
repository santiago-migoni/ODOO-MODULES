# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import fields, models


class ResUsersSettings(models.Model):
    _inherit = 'res.users.settings'

    homemenu_config = fields.Json(string="Home Menu Configuration", readonly=True)
    color_scheme = fields.Selection(
        [("system", "System"), ("light", "Light"), ("dark", "Dark")],
        default="system",
        required=True,
        string="Color Scheme",
    )
    dipl_quick_menu_favorites = fields.Json(
        string="Apps Favoritas (Acceso Rápido)",
        default=list,
        help="Lista de xmlids de apps marcadas como favoritas en el menú de acceso rápido.",
    )
