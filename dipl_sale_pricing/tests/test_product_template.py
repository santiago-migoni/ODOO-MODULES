# -*- coding: utf-8 -*-

from odoo.tests import TransactionCase
from odoo.exceptions import ValidationError


class TestProductTemplate(TransactionCase):
    """Tests para extensión de product.template"""

    def setUp(self):
        super().setUp()
        self.ProductTemplate = self.env['product.template']

    def test_create_producto_personalizado(self):
        """Test: Crear producto personalizado sincroniza list_price"""
        product = self.ProductTemplate.create({
            'name': 'Test Acero',
            'es_producto_personalizado': True,
            'precio_kg': 5000.0,
            'tipo_calculo': 'solo_kg',
            'densidad_material': 7.85,
            'espesor_mm': 3.0,
        })
        
        self.assertEqual(product.list_price, 5000.0)
        self.assertTrue(product.es_producto_personalizado)

    def test_write_precio_kg_actualiza_list_price(self):
        """Test: Modificar precio_kg actualiza list_price"""
        product = self.ProductTemplate.create({
            'name': 'Test Acero',
            'es_producto_personalizado': True,
            'precio_kg': 5000.0,
            'tipo_calculo': 'solo_kg',
        })
        
        product.write({'precio_kg': 6000.0})
        self.assertEqual(product.list_price, 6000.0)

    def test_producto_no_personalizado_no_sincroniza(self):
        """Test: Producto no personalizado mantiene list_price independiente"""
        product = self.ProductTemplate.create({
            'name': 'Test Normal',
            'es_producto_personalizado': False,
            'list_price': 10000.0,
            'precio_kg': 5000.0,
        })
        
        self.assertEqual(product.list_price, 10000.0)

    def test_validacion_densidad_negativa(self):
        """Test: Densidad negativa genera error"""
        with self.assertRaises(ValidationError):
            self.ProductTemplate.create({
                'name': 'Test',
                'densidad_material': -7.85,
            })

    def test_validacion_espesor_negativo(self):
        """Test: Espesor negativo genera error"""
        with self.assertRaises(ValidationError):
            self.ProductTemplate.create({
                'name': 'Test',
                'espesor_mm': -3.0,
            })

    def test_validacion_precio_kg_negativo(self):
        """Test: Precio kg negativo genera error"""
        with self.assertRaises(ValidationError):
            self.ProductTemplate.create({
                'name': 'Test',
                'precio_kg': -5000.0,
            })

    def test_validacion_precio_minuto_negativo(self):
        """Test: Precio minuto negativo genera error"""
        with self.assertRaises(ValidationError):
            self.ProductTemplate.create({
                'name': 'Test',
                'precio_minuto': -1000.0,
            })

    def test_marcar_personalizado_sincroniza(self):
        """Test: Marcar como personalizado sincroniza precio existente"""
        product = self.ProductTemplate.create({
            'name': 'Test',
            'es_producto_personalizado': False,
            'precio_kg': 5000.0,
            'list_price': 10000.0,
        })
        
        product.write({'es_producto_personalizado': True})
        self.assertEqual(product.list_price, 5000.0)

    def test_tipo_calculo_solo_kg(self):
        """Test: Tipo de cálculo solo_kg se configura correctamente"""
        product = self.ProductTemplate.create({
            'name': 'Test',
            'es_producto_personalizado': True,
            'tipo_calculo': 'solo_kg',
            'precio_kg': 5000.0,
        })
        
        self.assertEqual(product.tipo_calculo, 'solo_kg')

    def test_tipo_calculo_kg_mas_minutos(self):
        """Test: Tipo de cálculo kg_mas_minutos se configura correctamente"""
        product = self.ProductTemplate.create({
            'name': 'Test',
            'es_producto_personalizado': True,
            'tipo_calculo': 'kg_mas_minutos',
            'precio_kg': 5000.0,
            'precio_minuto': 1000.0,
        })
        
        self.assertEqual(product.tipo_calculo, 'kg_mas_minutos')
        self.assertEqual(product.precio_minuto, 1000.0)
