# -*- coding: utf-8 -*-

import logging
from odoo import models, fields, api
from odoo.exceptions import ValidationError

_logger = logging.getLogger(__name__)


class ProductTemplate(models.Model):
    _inherit = 'product.template'

    # Checkbox para identificar productos personalizados
    es_producto_personalizado = fields.Boolean(
        string='¿Es personalizado?',
        default=False,
        help='Marcar si el precio se calcula por peso y/o minutos de corte'
    )

    # Tipo de cálculo de precio
    tipo_calculo = fields.Selection([
        ('solo_kg', 'Solo por Kg'),
        ('kg_mas_minutos', 'Kg + Minutos de corte'),
    ], string='Tipo de Cálculo', default='solo_kg')

    # Precios
    precio_kg = fields.Monetary(
        string='Precio por Kg',
        currency_field='currency_id',
        help='Precio por kilogramo de material'
    )
    precio_minuto = fields.Monetary(
        string='Precio por Minuto',
        currency_field='currency_id',
        help='Precio por minuto de corte láser'
    )

    # Propiedades del material
    densidad_material = fields.Float(
        string='Densidad (g/cm³)',
        digits=(10, 4),
        default=7.85,
        help='Densidad del material. Ej: Acero = 7.85 g/cm³'
    )
    espesor_mm = fields.Float(
        string='Espesor (mm)',
        digits=(10, 2),
        help='Espesor del material en milímetros'
    )

    # Selector de material predefinido
    material_preset_id = fields.Many2one(
        'dipl_sale.material.preset',
        string='Material Predefinido',
        help='Seleccionar material común para autocompletar densidad'
    )

    # Dimensiones máximas
    max_desarrollo_mm = fields.Float(
        string='Desarrollo Máximo (mm)',
        digits=(10, 2),
        help='Desarrollo máximo permitido para este producto. 0 = sin límite'
    )
    max_largo_mm = fields.Float(
        string='Largo Máximo (mm)',
        digits=(10, 2),
        help='Largo máximo permitido para este producto. 0 = sin límite'
    )

    @api.onchange('precio_kg')
    def _onchange_precio_kg(self):
        """Sincroniza el precio de venta con el precio por kg"""
        if self.es_producto_personalizado and self.precio_kg:
            self.list_price = self.precio_kg

    @api.onchange('material_preset_id')
    def _onchange_material_preset(self):
        """Al seleccionar material predefinido, autocompletar densidad"""
        if self.material_preset_id:
            self.densidad_material = self.material_preset_id.density
            _logger.debug(
                f"Material preset '{self.material_preset_id.name}' seleccionado: "
                f"densidad={self.densidad_material}"
            )

    @api.onchange('es_producto_personalizado')
    def _onchange_es_producto_personalizado(self):
        """Al marcar como personalizado, sincroniza precios"""
        if self.es_producto_personalizado and self.precio_kg:
            self.list_price = self.precio_kg
        if not self.es_producto_personalizado:
            # Limpiar tipo de cálculo si se desmarca
            self.tipo_calculo = False

    @api.constrains('densidad_material', 'espesor_mm', 'precio_kg', 'precio_minuto')
    def _check_positive_values(self):
        for product in self:
            if product.densidad_material and product.densidad_material < 0:
                raise ValidationError('La densidad del material debe ser positiva.')
            if product.espesor_mm and product.espesor_mm < 0:
                raise ValidationError('El espesor debe ser positivo.')
            if product.precio_kg and product.precio_kg < 0:
                raise ValidationError('El precio por kg debe ser positivo.')
            if product.precio_minuto and product.precio_minuto < 0:
                raise ValidationError('El precio por minuto debe ser positivo.')

    def write(self, vals):
        """Al guardar, sincroniza list_price con precio_kg si es producto personalizado"""
        # Si se modifica precio_kg, actualizar list_price en la misma transacción
        if 'precio_kg' in vals:
            for product in self:
                # Verificar si es o será personalizado
                es_personalizado = vals.get('es_producto_personalizado', product.es_producto_personalizado)
                if es_personalizado:
                    vals['list_price'] = vals['precio_kg']
        
        # Si se marca como personalizado y ya tiene precio_kg
        if vals.get('es_producto_personalizado') and 'precio_kg' not in vals:
            for product in self:
                if product.precio_kg:
                    vals['list_price'] = product.precio_kg
        
        return super().write(vals)

    @api.model_create_multi
    def create(self, vals_list):
        """Al crear, sincroniza list_price con precio_kg"""
        for vals in vals_list:
            if vals.get('es_producto_personalizado') and vals.get('precio_kg'):
                vals['list_price'] = vals['precio_kg']
        return super().create(vals_list)
