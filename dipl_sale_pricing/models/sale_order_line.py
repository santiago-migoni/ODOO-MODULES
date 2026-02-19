# -*- coding: utf-8 -*-

import logging
import math
import re
from odoo import models, fields, api
from odoo.exceptions import ValidationError

# Constantes de conversión
MM3_TO_CM3 = 1000  # Conversión de mm³ a cm³
G_TO_KG = 1000     # Conversión de gramos a kilogramos
# ROUNDING_UNIT ahora es configurable (ver _get_rounding_unit)

_logger = logging.getLogger(__name__)


class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    # Dimensiones ingresadas por el vendedor (Float con calculadora via onchange)
    desarrollo_mm = fields.Float(
        string='Desarrollo (mm)',
        digits=(10, 2),
        help='Desarrollo de la pieza. Acepta expresiones: 1200 o 1100+50+50'
    )
    largo_mm = fields.Float(
        string='Largo (mm)',
        digits=(10, 2),
        help='Largo de la pieza. Acepta expresiones: 2000 o 1900+50+50'
    )
    minutos_corte = fields.Float(
        string='Minutos de Corte',
        digits=(10, 2),
        help='Tiempo de corte láser en minutos por unidad'
    )

    # Campos calculados
    peso_unitario = fields.Float(
        string='Peso Unitario (kg)',
        digits=(10, 4),
        compute='_compute_peso_precio',
        store=True,
        help='Peso por pieza en kilogramos'
    )
    peso_total = fields.Float(
        string='Peso Total (kg)',
        digits=(10, 2),
        compute='_compute_peso_precio',
        store=True,
        help='Peso total (peso unitario × cantidad)'
    )
    subtotal_material = fields.Monetary(
        string='Subtotal Material',
        compute='_compute_peso_precio',
        store=True,
        help='Costo del material (peso × $/kg)'
    )
    subtotal_corte = fields.Monetary(
        string='Subtotal Corte',
        compute='_compute_peso_precio',
        store=True,
        help='Costo del corte (minutos × $/min)'
    )

    # Control de visibilidad
    requiere_minutos = fields.Boolean(
        compute='_compute_requiere_minutos',
        store=True,
        help='Indica si el producto requiere minutos de corte'
    )

    # Flag para indicar si usar cálculo custom
    usa_calculo_peso = fields.Boolean(
        compute='_compute_usa_calculo_peso',
        store=True,
        help='Indica si esta línea usa cálculo por peso'
    )

    def _get_rounding_unit(self):
        """Obtiene la unidad de redondeo configurada"""
        rounding_unit = self.env['ir.config_parameter'].sudo().get_param(
            'dipl_sale_pricing.rounding_unit', '1000'
        )
        return int(rounding_unit)

    def _evaluar_expresion(self, expresion):
        """
        Evalúa una expresión matemática de forma segura.
        Soporta: +, -, *, /, (), números decimales
        Retorna el resultado o el valor original si no es expresión.
        
        Ejemplos:
            >>> self._evaluar_expresion("1200")
            1200.0
            >>> self._evaluar_expresion("1100+50+50")
            1200.0
            >>> self._evaluar_expresion("(100+200)*4")
            1200.0
        """
        if not expresion:
            return 0.0
        
        # Si ya es un número, retornarlo
        if isinstance(expresion, (int, float)):
            return float(expresion)
        
        expresion_str = str(expresion).strip().replace(',', '.')
        
        # Si es solo un número, retornarlo
        try:
            return float(expresion_str)
        except ValueError:
            pass
        
        # Validar que solo contiene caracteres permitidos
        patron_valido = r'^[\d\.\+\-\*\/\(\)\s]+$'
        if not re.match(patron_valido, expresion_str):
            _logger.warning(
                f"Expresión inválida '{expresion}': contiene caracteres no permitidos"
            )
            return 0.0
        
        try:
            # TODO: Migrar a simpleeval para mejor seguridad
            # from simpleeval import simple_eval
            # resultado = simple_eval(expresion_str)
            resultado = eval(expresion_str, {"__builtins__": {}}, {})
            _logger.debug(f"Expresión '{expresion}' evaluada a: {resultado}")
            return float(resultado) if resultado else 0.0
        except (ValueError, SyntaxError, ZeroDivisionError) as e:
            _logger.warning(f"Error evaluando expresión '{expresion}': {e}")
            return 0.0
        except Exception as e:
            _logger.error(f"Error inesperado evaluando '{expresion}': {e}")
            return 0.0

    def _redondear_a_miles(self, valor):
        """
        Redondea un valor a la unidad configurada (hacia arriba).
        
        Args:
            valor: Valor numérico a redondear
            
        Returns:
            int: Valor redondeado al múltiplo superior de la unidad configurada
            
        Ejemplos:
            Con ROUNDING_UNIT=1000:
            >>> self._redondear_a_miles(1234)
            2000
            Con ROUNDING_UNIT=100:
            >>> self._redondear_a_miles(1234)
            1300
        """
        if not valor:
            return 0
        rounding_unit = self._get_rounding_unit()
        return math.ceil(valor / rounding_unit) * rounding_unit

    @api.constrains('desarrollo_mm', 'largo_mm', 'minutos_corte')
    def _check_positive_dimensions(self):
        """Valida que dimensiones sean positivas y dentro de límites"""
        enable_validation = self.env['ir.config_parameter'].sudo().get_param(
            'dipl_sale_pricing.enable_dimension_validation', 'False'
        )
        
        for line in self:
            # Validar positivos
            if line.desarrollo_mm and line.desarrollo_mm < 0:
                raise ValidationError('El desarrollo debe ser positivo.')
            if line.largo_mm and line.largo_mm < 0:
                raise ValidationError('El largo debe ser positivo.')
            if line.minutos_corte and line.minutos_corte < 0:
                raise ValidationError('Los minutos de corte deben ser positivos.')
            
            # Validar dimensiones máximas si está habilitado
            if enable_validation == 'True' and line.product_id:
                product = line.product_id
                
                # Verificar desarrollo máximo (producto o global)
                max_desarrollo = product.max_desarrollo_mm
                if not max_desarrollo:
                    max_desarrollo = float(self.env['ir.config_parameter'].sudo().get_param(
                        'dipl_sale_pricing.max_desarrollo_global', '0'
                    ))
                
                if max_desarrollo > 0 and line.desarrollo_mm > max_desarrollo:
                    raise ValidationError(
                        f'El desarrollo ({line.desarrollo_mm:.0f} mm) excede el máximo '
                        f'permitido ({max_desarrollo:.0f} mm) para este producto.'
                    )
                
                # Verificar largo máximo (producto o global)
                max_largo = product.max_largo_mm
                if not max_largo:
                    max_largo = float(self.env['ir.config_parameter'].sudo().get_param(
                        'dipl_sale_pricing.max_largo_global', '0'
                    ))
                
                if max_largo > 0 and line.largo_mm > max_largo:
                    raise ValidationError(
                        f'El largo ({line.largo_mm:.0f} mm) excede el máximo '
                        f'permitido ({max_largo:.0f} mm) para este producto.'
                    )

    @api.depends('product_id.tipo_calculo')
    def _compute_requiere_minutos(self):
        for line in self:
            line.requiere_minutos = (
                line.product_id.tipo_calculo == 'kg_mas_minutos'
            )

    @api.depends('desarrollo_mm', 'largo_mm', 'product_id.tipo_calculo')
    def _compute_usa_calculo_peso(self):
        for line in self:
            line.usa_calculo_peso = bool(
                line.desarrollo_mm and 
                line.largo_mm and 
                line.product_id.tipo_calculo
            )

    @api.depends(
        'desarrollo_mm', 'largo_mm', 'minutos_corte', 'product_uom_qty',
        'product_id.densidad_material', 'product_id.espesor_mm',
        'product_id.precio_kg', 'product_id.precio_minuto',
        'product_id.tipo_calculo', 'currency_id'
    )
    def _compute_peso_precio(self):
        for line in self:
            product = line.product_id

            # Calcular peso unitario (kg)
            if (line.desarrollo_mm and line.largo_mm and 
                product.espesor_mm and product.densidad_material):
                # Fórmula: (desarrollo × largo × espesor) mm³ → cm³ → g → kg
                volumen_mm3 = line.desarrollo_mm * line.largo_mm * product.espesor_mm
                volumen_cm3 = volumen_mm3 / MM3_TO_CM3
                peso_g = volumen_cm3 * product.densidad_material
                line.peso_unitario = peso_g / G_TO_KG
                
                _logger.debug(
                    f"Calculado peso unitario para línea {line.id}: "
                    f"vol={volumen_mm3:.0f}mm³, peso={line.peso_unitario:.4f}kg"
                )
            else:
                line.peso_unitario = 0

            # Peso total
            line.peso_total = line.peso_unitario * line.product_uom_qty

            # Subtotal material
            line.subtotal_material = line.peso_total * (product.precio_kg or 0)

            # Subtotal corte (solo si aplica). Ahora minutos_corte es por UNIDAD
            if product.tipo_calculo == 'kg_mas_minutos':
                line.subtotal_corte = line.product_uom_qty * line.minutos_corte * (product.precio_minuto or 0)
            else:
                line.subtotal_corte = 0

    def _get_precio_unitario_redondeado(self):
        """
        Calcula el precio unitario redondeado basado en peso y dimensiones.
        El redondeo se aplica ANTES del descuento.
        
        Flujo:
        1. Calcular costo base (material + corte)
        2. Redondear ese costo
        3. Dividir por cantidad para obtener precio unitario
        4. Odoo aplicará el descuento automáticamente sobre este precio
        """
        self.ensure_one()
        
        # Paso 1: Costo base total
        total_sin_redondear = self.subtotal_material + self.subtotal_corte
        
        # Paso 2: Redondear
        total_redondeado = self._redondear_a_miles(total_sin_redondear)
        
        # Paso 3: Precio unitario = total redondeado / cantidad
        if self.product_uom_qty:
            return total_redondeado / self.product_uom_qty
        return 0.0

    @api.onchange('desarrollo_mm', 'largo_mm', 'minutos_corte', 'product_uom_qty')
    def _onchange_dimensiones(self):
        """
        Actualiza el precio unitario cuando cambian las dimensiones.
        
        Nueva lógica simplificada:
        - Calcula costo base (material + corte)
        - Redondea ese costo
        - Divide por cantidad = price_unit
        - Odoo aplica el descuento automáticamente
        """
        if self.usa_calculo_peso and self.product_uom_qty:
            self.price_unit = self._get_precio_unitario_redondeado()

    def _prepare_base_line_for_taxes_computation(self, **kwargs):
        """Override para usar nuestro cálculo de precio cuando aplica"""
        self.ensure_one()
        
        # Si usamos cálculo por peso, usar el precio unitario redondeado
        if self.usa_calculo_peso:
            kwargs['price_unit'] = self._get_precio_unitario_redondeado()
            kwargs['discount'] = self.discount
        
        return super()._prepare_base_line_for_taxes_computation(**kwargs)

    @api.model_create_multi
    def create(self, vals_list):
        """Al crear, evaluar expresiones y actualizar price_unit"""
        for vals in vals_list:
            # Evaluar expresiones en desarrollo y largo
            if 'desarrollo_mm' in vals:
                vals['desarrollo_mm'] = self._evaluar_expresion(vals['desarrollo_mm'])
            if 'largo_mm' in vals:
                vals['largo_mm'] = self._evaluar_expresion(vals['largo_mm'])
        
        lines = super().create(vals_list)
        for line in lines:
            if line.usa_calculo_peso and line.product_uom_qty:
                line.price_unit = line._get_precio_unitario_redondeado()
        return lines

    def write(self, vals):
        """Al guardar, evaluar expresiones y actualizar price_unit"""
        # Evaluar expresiones en desarrollo y largo
        if 'desarrollo_mm' in vals:
            vals['desarrollo_mm'] = self._evaluar_expresion(vals['desarrollo_mm'])
        if 'largo_mm' in vals:
            vals['largo_mm'] = self._evaluar_expresion(vals['largo_mm'])
        
        result = super().write(vals)
        dimension_fields = {'desarrollo_mm', 'largo_mm', 'minutos_corte', 'product_uom_qty'}
        if dimension_fields & set(vals.keys()):
            for line in self:
                if line.usa_calculo_peso and line.product_uom_qty:
                    new_price = line._get_precio_unitario_redondeado()
                    # Usar SQL para evitar recursión
                    self.env.cr.execute(
                        "UPDATE sale_order_line SET price_unit = %s WHERE id = %s",
                        (new_price, line.id)
                    )
            self.invalidate_recordset(['price_unit'])
        return result
