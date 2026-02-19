# -*- coding: utf-8 -*-

from odoo.tests import TransactionCase


class TestExpressions(TransactionCase):
    """Tests para evaluación de expresiones matemáticas"""

    def setUp(self):
        super().setUp()
        self.SaleOrderLine = self.env['sale.order.line']
        # Crear línea vacía para usar métodos de instancia
        self.line = self.SaleOrderLine.new({})

    def test_evaluar_expresion_simple(self):
        """Test: Número simple se convierte correctamente"""
        result = self.line._evaluar_expresion("1200")
        self.assertEqual(result, 1200.0)

    def test_evaluar_expresion_float(self):
        """Test: Número decimal se convierte correctamente"""
        result = self.line._evaluar_expresion("1200.5")
        self.assertEqual(result, 1200.5)

    def test_evaluar_expresion_suma(self):
        """Test: Suma simple: 1100+50+50 = 1200"""
        result = self.line._evaluar_expresion("1100+50+50")
        self.assertEqual(result, 1200.0)

    def test_evaluar_expresion_resta(self):
        """Test: Resta: 2000-100 = 1900"""
        result = self.line._evaluar_expresion("2000-100")
        self.assertEqual(result, 1900.0)

    def test_evaluar_expresion_multiplicacion(self):
        """Test: Multiplicación: 100*12 = 1200"""
        result = self.line._evaluar_expresion("100*12")
        self.assertEqual(result, 1200.0)

    def test_evaluar_expresion_division(self):
        """Test: División: 2400/2 = 1200"""
        result = self.line._evaluar_expresion("2400/2")
        self.assertEqual(result, 1200.0)

    def test_evaluar_expresion_parentesis(self):
        """Test: Expresión con paréntesis: (100+200)*4 = 1200"""
        result = self.line._evaluar_expresion("(100+200)*4")
        self.assertEqual(result, 1200.0)

    def test_evaluar_expresion_compleja(self):
        """Test: Expresión compleja: (1000+100)*2-400+200 = 2000"""
        result = self.line._evaluar_expresion("(1000+100)*2-400+200")
        self.assertEqual(result, 2000.0)

    def test_evaluar_expresion_vacia(self):
        """Test: Expresión vacía retorna 0"""
        result = self.line._evaluar_expresion("")
        self.assertEqual(result, 0.0)

    def test_evaluar_expresion_none(self):
        """Test: None retorna 0"""
        result = self.line._evaluar_expresion(None)
        self.assertEqual(result, 0.0)

    def test_evaluar_expresion_invalida(self):
        """Test: Expresión inválida retorna 0"""
        result = self.line._evaluar_expresion("abc")
        self.assertEqual(result, 0.0)

    def test_evaluar_expresion_numero_ya_float(self):
        """Test: Si ya es float, lo retorna"""
        result = self.line._evaluar_expresion(1200.5)
        self.assertEqual(result, 1200.5)

    def test_evaluar_expresion_numero_ya_int(self):
        """Test: Si ya es int, lo convierte a float"""
        result = self.line._evaluar_expresion(1200)
        self.assertEqual(result, 1200.0)

    def test_redondear_a_miles_simple(self):
        """Test: 1234 redondea a 2000"""
        result = self.line._redondear_a_miles(1234)
        self.assertEqual(result, 2000)

    def test_redondear_a_miles_mayor(self):
        """Test: 5678 redondea a 6000"""
        result = self.line._redondear_a_miles(5678)
        self.assertEqual(result, 6000)

    def test_redondear_a_miles_exacto(self):
        """Test: 5000 se mantiene en 5000"""
        result = self.line._redondear_a_miles(5000)
        self.assertEqual(result, 5000)

    def test_redondear_a_miles_casi_mil(self):
        """Test: 999 redondea a 1000"""
        result = self.line._redondear_a_miles(999)
        self.assertEqual(result, 1000)

    def test_redondear_a_miles_uno_mas(self):
        """Test: 10001 redondea a 11000"""
        result = self.line._redondear_a_miles(10001)
        self.assertEqual(result, 11000)

    def test_redondear_a_miles_cero(self):
        """Test: 0 se mantiene en 0"""
        result = self.line._redondear_a_miles(0)
        self.assertEqual(result, 0)

    def test_redondear_a_miles_none(self):
        """Test: None retorna 0"""
        result = self.line._redondear_a_miles(None)
        self.assertEqual(result, 0)
