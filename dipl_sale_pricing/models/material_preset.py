# -*- coding: utf-8 -*-

import logging
from odoo import models, fields

_logger = logging.getLogger(__name__)


class MaterialPreset(models.Model):
    _name = 'dipl_sale.material.preset'
    _description = 'Densidades predefinidas de materiales'
    _order = 'sequence, name'

    sequence = fields.Integer('Secuencia', default=10)
    name = fields.Char('Material', required=True, translate=True)
    density = fields.Float(
        'Densidad (g/cm³)',
        required=True,
        digits=(10, 4),
        help='Densidad del material en gramos por centímetro cúbico'
    )
    description = fields.Text('Descripción', translate=True)
    active = fields.Boolean('Activo', default=True)

    _sql_constraints = [
        ('name_unique', 'UNIQUE(name)', 'Ya existe un material con ese nombre.'),
        ('density_positive', 'CHECK(density > 0)', 'La densidad debe ser positiva.'),
    ]
