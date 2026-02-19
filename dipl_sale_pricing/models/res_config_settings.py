# -*- coding: utf-8 -*-

import logging
from odoo import models, fields, api

_logger = logging.getLogger(__name__)


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    # Configuración de redondeo
    rounding_unit = fields.Selection([
        ('10', 'Decenas'),
        ('100', 'Centenas'),
        ('1000', 'Miles'),
        ('10000', 'Decenas de Miles'),
    ], string='Unidad de Redondeo', 
       default='1000',
       config_parameter='dipl_sale_pricing.rounding_unit',
       help='Unidad a la que se redondearán los precios calculados')

    # Configuración de validaciones
    enable_dimension_validation = fields.Boolean(
        string='Validar Dimensiones Máximas',
        config_parameter='dipl_sale_pricing.enable_dimension_validation',
        help='Activar validación de dimensiones máximas según capacidad de máquinas'
    )

    max_desarrollo_global = fields.Float(
        string='Desarrollo Máximo Global (mm)',
        config_parameter='dipl_sale_pricing.max_desarrollo_global',
        default=3000.0,
        help='Desarrollo máximo permitido por defecto'
    )

    max_largo_global = fields.Float(
        string='Largo Máximo Global (mm)',
        config_parameter='dipl_sale_pricing.max_largo_global',
        default=6000.0,
        help='Largo máximo permitido por defecto'
    )

    # Uso de densidades predefinidas
    use_material_presets = fields.Boolean(
        string='Usar Densidades Predefinidas',
        config_parameter='dipl_sale_pricing.use_material_presets',
        default=True,
        help='Ofrecer selección rápida de materiales comunes'
    )
