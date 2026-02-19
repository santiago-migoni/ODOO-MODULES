# -*- coding: utf-8 -*-

from odoo.tests import TransactionCase
from odoo.exceptions import ValidationError


class TestSaleOrderLine(TransactionCase):
    """Tests para extensión de sale.order.line"""

    def setUp(self):
        super().setUp()
        # Crear producto personalizado para tests
        self.product = self.env['product.template'].create({
            'name': 'Acero Test',
            'es_producto_personalizado': True,
            'tipo_calculo': 'solo_kg',
            'precio_kg': 5000.0,
            'densidad_material': 7.85,  # g/cm³
            'espesor_mm': 3.0,
        })
        
        # Crear orden de venta
        self.partner = self.env['res.partner'].create({
            'name': 'Cliente Test'
        })
        self.order = self.env['sale.order'].create({
            'partner_id': self.partner.id,
        })

    def test_calculo_peso_unitario(self):
        """Test: Cálculo correcto de peso unitario"""
        line = self.env['sale.order.line'].create({
            'order_id': self.order.id,
            'product_id': self.product.product_variant_id.id,
            'producto_uom_qty': 1,
            'desarrollo_mm': 1200.0,
            'largo_mm': 2000.0,
        })
        
        # Peso esperado:
        # Volumen = 1200 * 2000 * 3 = 7,200,000 mm³
        # Volumen = 7,200,000 / 1000 = 7,200 cm³
        # Peso = 7,200 * 7.85 = 56,520 g
        # Peso = 56,520 / 1000 = 56.52 kg
        self.assertAlmostEqual(line.peso_unitario, 56.52, places=2)

    def test_calculo_peso_total(self):
        """Test: Peso total = peso unitario × cantidad"""
        line = self.env['sale.order.line'].create({
            'order_id': self.order.id,
            'product_id': self.product.product_variant_id.id,
            'product_uom_qty': 10,
            'desarrollo_mm': 1200.0,
            'largo_mm': 2000.0,
        })
        
        self.assertAlmostEqual(line.peso_total, 565.2, places=1)

    def test_calculo_subtotal_material(self):
        """Test: Subtotal material = peso total × precio/kg"""
        line = self.env['sale.order.line'].create({
            'order_id': self.order.id,
            'product_id': self.product.product_variant_id.id,
            'product_uom_qty': 10,
            'desarrollo_mm': 1200.0,
            'largo_mm': 2000.0,
        })
        
        # 565.2 kg * $5000/kg = $2,826,000
        self.assertAlmostEqual(line.subtotal_material, 2826000, places=0)

    def test_producto_con_minutos(self):
        """Test: Producto con minutos de corte calcula subtotal_corte"""
        product_minutos = self.env['product.template'].create({
            'name': 'Acero con Laser',
            'es_producto_personalizado': True,
            'tipo_calculo': 'kg_mas_minutos',
            'precio_kg': 5000.0,
            'precio_minuto': 1000.0,
            'densidad_material': 7.85,
            'espesor_mm': 3.0,
        })
        
        line = self.env['sale.order.line'].create({
            'order_id': self.order.id,
            'product_id': product_minutos.product_variant_id.id,
            'product_uom_qty': 10,
            'desarrollo_mm': 1200.0,
            'largo_mm': 2000.0,
            'minutos_corte': 5.0,  # 5 minutos por unidad
        })
        
        # Subtotal corte = 10 unidades × 5 min/unidad × $1000/min = $50,000
        self.assertEqual(line.subtotal_corte, 50000)

    def test_validacion_desarrollo_negativo(self):
        """Test: Desarrollo negativo genera error"""
        with self.assertRaises(ValidationError):
            self.env['sale.order.line'].create({
                'order_id': self.order.id,
                'product_id': self.product.product_variant_id.id,
                'product_uom_qty': 1,
                'desarrollo_mm': -1200.0,
                'largo_mm': 2000.0,
            })

    def test_validacion_largo_negativo(self):
        """Test: Largo negativo genera error"""
        with self.assertRaises(ValidationError):
            self.env['sale.order.line'].create({
                'order_id': self.order.id,
                'product_id': self.product.product_variant_id.id,
                'product_uom_qty': 1,
                'desarrollo_mm': 1200.0,
                'largo_mm': -2000.0,
            })

    def test_validacion_minutos_negativos(self):
        """Test: Minutos negativos genera error"""
        with self.assertRaises(ValidationError):
            self.env['sale.order.line'].create({
                'order_id': self.order.id,
                'product_id': self.product.product_variant_id.id,
                'product_uom_qty': 1,
                'desarrollo_mm': 1200.0,
                'largo_mm': 2000.0,
                'minutos_corte': -5.0,
            })

    def test_expresion_en_desarrollo(self):
        """Test: Expresión matemática en desarrollo se evalúa correctamente"""
        line = self.env['sale.order.line'].create({
            'order_id': self.order.id,
            'product_id': self.product.product_variant_id.id,
            'product_uom_qty': 1,
            'desarrollo_mm': '1100+50+50',  # = 1200
            'largo_mm': 2000.0,
        })
        
        self.assertEqual(line.desarrollo_mm, 1200.0)

    def test_expresion_en_largo(self):
        """Test: Expresión matemática en largo se evalúa correctamente"""
        line = self.env['sale.order.line'].create({
            'order_id': self.order.id,
            'product_id': self.product.product_variant_id.id,
            'product_uom_qty': 1,
            'desarrollo_mm': 1200.0,
            'largo_mm': '2000-100',  # = 1900
        })
        
        self.assertEqual(line.largo_mm, 1900.0)

    def test_usa_calculo_peso_true(self):
        """Test: usa_calculo_peso es True cuando hay dimensiones y tipo_calculo"""
        line = self.env['sale.order.line'].create({
            'order_id': self.order.id,
            'product_id': self.product.product_variant_id.id,
            'product_uom_qty': 1,
            'desarrollo_mm': 1200.0,
            'largo_mm': 2000.0,
        })
        
        self.assertTrue(line.usa_calculo_peso)

    def test_requiere_minutos_false_solo_kg(self):
        """Test: requiere_minutos es False para tipo solo_kg"""
        line = self.env['sale.order.line'].create({
            'order_id': self.order.id,
            'product_id': self.product.product_variant_id.id,
            'product_uom_qty': 1,
        })
        
        self.assertFalse(line.requiere_minutos)

    def test_requiere_minutos_true_kg_mas_minutos(self):
        """Test: requiere_minutos es True para tipo kg_mas_minutos"""
        product_minutos = self.env['product.template'].create({
            'name': 'Test',
            'es_producto_personalizado': True,
            'tipo_calculo': 'kg_mas_minutos',
            'precio_kg': 5000.0,
            'precio_minuto': 1000.0,
        })
        
        line = self.env['sale.order.line'].create({
            'order_id': self.order.id,
            'product_id': product_minutos.product_variant_id.id,
            'product_uom_qty': 1,
        })
        
        self.assertTrue(line.requiere_minutos)
