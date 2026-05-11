from odoo.tests.common import TransactionCase


class TestTechnicalQuoteModuleInstall(TransactionCase):
    def test_technical_quote_product_fields_exist(self):
        product = self.env["product.template"]
        self.assertIn("dipl_is_technical_quote_product", product._fields)
        self.assertIn("dipl_geometric_factor", product._fields)
        self.assertIn("dipl_theoretical_kg", product._fields)
        self.assertNotIn("dipl_price_per_kg", product._fields)
        self.assertNotIn("dipl_material_code", product._fields)
        self.assertNotIn("dipl_thickness_label", product._fields)
        self.assertNotIn("dipl_requires_dimensions", product._fields)
        self.assertNotIn("dipl_technical_notes", product._fields)

    def test_sale_order_line_technical_fields_exist(self):
        line = self.env["sale.order.line"]
        self.assertIn("dipl_is_technical_line", line._fields)
        self.assertIn("dipl_development_mm", line._fields)
        self.assertIn("dipl_width_mm", line._fields)
        self.assertNotIn("dipl_material_code", line._fields)
        self.assertNotIn("dipl_thickness_label", line._fields)
        self.assertNotIn("dipl_thickness_mm", line._fields)
        self.assertNotIn("dipl_material_density", line._fields)
        self.assertIn("dipl_theoretical_kg", line._fields)
        self.assertIn("dipl_price_per_kg", line._fields)
        self.assertNotIn("dipl_kg_computed", line._fields)
        self.assertIn("dipl_kg_total", line._fields)
        self.assertIn("dipl_kg_mode", line._fields)
        self.assertIn("dipl_technical_total", line._fields)
        self.assertIn("dipl_technical_price_unit", line._fields)
        self.assertIn("dipl_can_compute", line._fields)
        self.assertNotIn("dipl_has_manual_final_price", line._fields)
        self.assertIn("dipl_pricing_state", line._fields)
        self.assertNotIn("dipl_use_manual_kg", line._fields)
        self.assertNotIn("dipl_kg_manual", line._fields)

    def test_sale_report_technical_kg_measure_exists(self):
        report = self.env["sale.report"]
        self.assertIn("dipl_kg_total", report._fields)
