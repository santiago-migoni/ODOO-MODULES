from odoo.exceptions import ValidationError
from odoo.tests.common import TransactionCase


class TestTechnicalQuoteSaleOrderLineSnapshot(TransactionCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.partner = cls.env["res.partner"].create({"name": "Snapshot Customer"})
        cls.product_technical_a = cls.env["product.template"].create(
            {
                "name": "Tech Product A",
                "sale_ok": True,
                "list_price": 100.0,
                "dipl_is_technical_quote_product": True,
                "dipl_thickness_mm": 1.2,
                "dipl_material_density": 7.85,
                "dipl_geometric_factor": 1.0,
            }
        )
        cls.product_technical_b = cls.env["product.template"].create(
            {
                "name": "Tech Product B",
                "sale_ok": True,
                "list_price": 125.0,
                "dipl_is_technical_quote_product": True,
                "dipl_thickness_mm": 1.6,
                "dipl_material_density": 8.15,
                "dipl_geometric_factor": 1.0,
            }
        )
        cls.product_standard = cls.env["product.template"].create(
            {
                "name": "Standard Product",
                "sale_ok": True,
            }
        )
        cls.order = cls.env["sale.order"].create({"partner_id": cls.partner.id})

    def _create_pricelist(self, name, **extra_vals):
        vals = {
            "name": name,
            "currency_id": self.order.currency_id.id,
        }
        vals.update(extra_vals)
        return self.env["product.pricelist"].create(vals)

    def _create_geometry_line(self, **extra_vals):
        vals = {
            "order_id": self.order.id,
            "product_id": self.product_technical_a.product_variant_id.id,
            "product_uom_qty": 2.0,
            "dipl_development_mm": 100.0,
            "dipl_width_mm": 50.0,
            "name": "Tech geometry line",
        }
        vals.update(extra_vals)
        return self.env["sale.order.line"].create(vals)

    def _create_incomplete_line(self, **extra_vals):
        vals = {
            "order_id": self.order.id,
            "product_id": self.product_technical_a.product_variant_id.id,
            "product_uom_qty": 2.0,
            "name": "Tech incomplete line",
        }
        vals.update(extra_vals)
        return self.env["sale.order.line"].create(vals)

    def test_snapshot_is_copied_on_create(self):
        line = self.env["sale.order.line"].create(
            {
                "order_id": self.order.id,
                "product_id": self.product_technical_a.product_variant_id.id,
                "product_uom_qty": 1.0,
                "name": "Tech line",
            }
        )
        self.assertTrue(line.dipl_is_technical_line)
        self.assertEqual(line.dipl_theoretical_kg, 9.42)
        self.assertEqual(line.dipl_price_per_kg, 100.0)

    def test_snapshot_is_replaced_when_product_changes(self):
        line = self._create_geometry_line(product_uom_qty=1.0, name="Tech line change")
        line.write({"product_id": self.product_technical_b.product_variant_id.id})
        self.assertTrue(line.dipl_is_technical_line)
        self.assertEqual(line.dipl_theoretical_kg, 13.04)
        self.assertEqual(line.dipl_price_per_kg, 125.0)
        self.assertEqual(line.dipl_kg_mode, "geometry")
        self.assertAlmostEqual(line.dipl_technical_price_unit, 8.15, places=2)
        self.assertAlmostEqual(line.price_unit, 8.15, places=2)

    def test_snapshot_is_cleared_when_switching_to_non_technical_product(self):
        line = self.env["sale.order.line"].create(
            {
                "order_id": self.order.id,
                "product_id": self.product_technical_a.product_variant_id.id,
                "product_uom_qty": 1.0,
                "name": "Tech line clear",
            }
        )
        line.write({"product_id": self.product_standard.product_variant_id.id})
        self.assertFalse(line.dipl_is_technical_line)
        self.assertFalse(line.dipl_kg_mode)
        self.assertEqual(line.dipl_theoretical_kg, 0.0)
        self.assertEqual(line.dipl_price_per_kg, 0.0)

    def test_snapshot_is_not_resynced_after_product_update(self):
        line = self.env["sale.order.line"].create(
            {
                "order_id": self.order.id,
                "product_id": self.product_technical_a.product_variant_id.id,
                "product_uom_qty": 1.0,
                "name": "Tech line frozen",
            }
        )
        self.product_technical_a.write({"list_price": 200.0})
        line.invalidate_recordset(["dipl_price_per_kg"])
        self.assertEqual(line.dipl_price_per_kg, 100.0)

    def test_snapshot_stays_available_after_reload(self):
        line = self._create_geometry_line(name="Tech line reload snapshot")
        line.invalidate_recordset(
            [
                "dipl_theoretical_kg",
                "dipl_price_per_kg",
                "dipl_kg_total",
            ]
        )
        self.assertEqual(line.dipl_theoretical_kg, 9.42)
        self.assertEqual(line.dipl_price_per_kg, 100.0)
        self.assertAlmostEqual(line.dipl_kg_total, 0.0942, places=4)

    def test_inconsistent_snapshot_is_rehydrated_on_write(self):
        line = self._create_geometry_line(name="Tech line rehydrate snapshot")
        line.write(
            {
                "dipl_theoretical_kg": 0.0,
                "dipl_price_per_kg": 0.0,
            }
        )
        self.assertEqual(line.dipl_kg_total, 0.0)
        line.write({"name": "Tech line rehydrated"})
        self.assertEqual(line.dipl_theoretical_kg, 9.42)
        self.assertEqual(line.dipl_price_per_kg, 100.0)
        self.assertAlmostEqual(line.dipl_kg_total, 0.0942, places=4)

    def test_partial_write_cannot_degrade_healthy_snapshot(self):
        line = self._create_geometry_line(name="Tech line protect healthy snapshot")
        self.assertAlmostEqual(line.dipl_kg_total, 0.0942, places=4)
        line.write(
            {
                "dipl_theoretical_kg": 0.0,
                "dipl_price_per_kg": 0.0,
                "dipl_width_mm": 75.0,
            }
        )
        self.assertEqual(line.dipl_theoretical_kg, 9.42)
        self.assertEqual(line.dipl_price_per_kg, 100.0)
        self.assertAlmostEqual(line.dipl_kg_total, 0.1413, places=4)

    def test_theoretical_kilograms_are_computed_on_product(self):
        self.assertAlmostEqual(
            self.product_technical_a.dipl_theoretical_kg, 9.42, places=2
        )
        self.product_technical_a.dipl_geometric_factor = 0.5
        self.assertAlmostEqual(
            self.product_technical_a.dipl_theoretical_kg, 4.71, places=2
        )

    def test_technical_products_require_geometric_factor(self):
        with self.assertRaises(ValidationError):
            self.env["product.template"].create(
                {
                    "name": "Tech Product Missing Factor",
                    "sale_ok": True,
                    "list_price": 100.0,
                    "dipl_is_technical_quote_product": True,
                    "dipl_thickness_mm": 1.2,
                    "dipl_material_density": 7.85,
                }
            )

    def test_geometry_mode_computes_kilograms_by_default(self):
        line = self._create_geometry_line(name="Tech line geometry mode")
        self.assertEqual(line.dipl_kg_mode, "geometry")
        self.assertAlmostEqual(line.dipl_kg_computed, 0.0942, places=4)
        self.assertAlmostEqual(line.dipl_kg_total, line.dipl_kg_computed, places=4)
        self.assertAlmostEqual(line.dipl_technical_total, 9.42, places=2)
        self.assertAlmostEqual(line.dipl_technical_price_unit, 4.71, places=2)
        self.assertAlmostEqual(line.price_unit, 4.71, places=2)
        self.assertAlmostEqual(line.technical_price_unit, 4.71, places=2)
        self.assertEqual(line.dipl_pricing_state, "technical")

    def test_incomplete_line_with_no_dimensions_stays_allowed_and_incomplete(self):
        line = self._create_incomplete_line()
        self.assertEqual(line.dipl_kg_mode, "incomplete")
        self.assertEqual(line.dipl_kg_computed, 0.0)
        self.assertEqual(line.dipl_kg_total, 0.0)
        self.assertEqual(line.dipl_technical_total, 0.0)
        self.assertEqual(line.dipl_technical_price_unit, 0.0)
        self.assertEqual(line.price_unit, 0.0)
        self.assertEqual(line.dipl_pricing_state, "incomplete")

    def test_incomplete_line_with_single_dimension_stays_allowed_and_incomplete(self):
        line = self._create_incomplete_line(dipl_development_mm=100.0)
        self.assertEqual(line.dipl_kg_mode, "incomplete")
        self.assertEqual(line.dipl_kg_total, 0.0)
        self.assertEqual(line.dipl_technical_price_unit, 0.0)
        self.assertEqual(line.price_unit, 0.0)
        self.assertEqual(line.dipl_pricing_state, "incomplete")

    def test_completing_missing_dimension_recovers_geometry_calculation(self):
        line = self._create_incomplete_line(dipl_development_mm=100.0)
        self.assertEqual(line.dipl_kg_mode, "incomplete")
        line.write({"dipl_width_mm": 50.0})
        self.assertEqual(line.dipl_kg_mode, "geometry")
        self.assertAlmostEqual(line.dipl_kg_total, 0.0942, places=4)
        self.assertAlmostEqual(line.price_unit, 4.71, places=2)
        self.assertEqual(line.dipl_pricing_state, "technical")

    def test_clearing_dimension_switches_geometry_line_to_incomplete(self):
        line = self._create_geometry_line(name="Tech line geometry to incomplete")
        line.write({"dipl_width_mm": 0.0})
        self.assertEqual(line.dipl_kg_mode, "incomplete")
        self.assertEqual(line.dipl_kg_total, 0.0)
        self.assertEqual(line.price_unit, 0.0)
        self.assertEqual(line.dipl_pricing_state, "incomplete")

    def test_changing_line_price_per_kg_recomputes_native_price_unit(self):
        line = self._create_geometry_line(name="Tech line price per kg update")
        line.write({"dipl_price_per_kg": 200.0})
        self.assertAlmostEqual(line.dipl_technical_total, 18.84, places=2)
        self.assertAlmostEqual(line.dipl_technical_price_unit, 9.42, places=2)
        self.assertAlmostEqual(line.price_unit, 9.42, places=2)
        self.assertAlmostEqual(line.technical_price_unit, 9.42, places=2)

    def test_non_technical_lines_keep_native_price_logic(self):
        self.product_standard.write({"list_price": 42.0})
        line = self.env["sale.order.line"].create(
            {
                "order_id": self.order.id,
                "product_id": self.product_standard.product_variant_id.id,
                "product_uom_qty": 3.0,
                "name": "Standard line",
            }
        )
        self.assertFalse(line.dipl_is_technical_line)
        self.assertAlmostEqual(line.price_unit, 42.0, places=2)
        self.assertAlmostEqual(line.technical_price_unit, 42.0, places=2)

    def test_discount_remains_usable_on_technical_lines(self):
        line = self._create_geometry_line(name="Tech line discount")
        line.write({"discount": 10.0})
        self.assertEqual(line.discount, 10.0)
        self.assertAlmostEqual(line.price_unit, line.dipl_technical_price_unit, places=4)

    def test_percentage_pricelist_applies_over_technical_base(self):
        pricelist = self._create_pricelist("Tech %")
        rule = self.env["product.pricelist.item"].create(
            {
                "pricelist_id": pricelist.id,
                "applied_on": "1_product",
                "product_tmpl_id": self.product_technical_a.id,
                "compute_price": "percentage",
                "percent_price": 10.0,
            }
        )
        order = self.env["sale.order"].create(
            {
                "partner_id": self.partner.id,
                "pricelist_id": pricelist.id,
            }
        )
        line = self.env["sale.order.line"].create(
            {
                "order_id": order.id,
                "product_id": self.product_technical_a.product_variant_id.id,
                "product_uom_qty": 2.0,
                "dipl_development_mm": 100.0,
                "dipl_width_mm": 50.0,
                "name": "Tech line percentage pricelist",
            }
        )
        effective_unit_price = line.price_unit * (1 - (line.discount or 0.0) / 100.0)
        self.assertEqual(line.pricelist_item_id, rule)
        self.assertAlmostEqual(line.dipl_technical_price_unit, 4.71, places=2)
        self.assertAlmostEqual(effective_unit_price, 4.239, places=3)
        self.assertEqual(line.dipl_pricing_state, "pricelist_adjusted")

    def test_formula_pricelist_applies_over_technical_base(self):
        pricelist = self._create_pricelist("Tech Formula")
        rule = self.env["product.pricelist.item"].create(
            {
                "pricelist_id": pricelist.id,
                "applied_on": "1_product",
                "product_tmpl_id": self.product_technical_a.id,
                "compute_price": "formula",
                "base": "list_price",
                "price_discount": 10.0,
                "price_surcharge": 1.5,
            }
        )
        order = self.env["sale.order"].create(
            {
                "partner_id": self.partner.id,
                "pricelist_id": pricelist.id,
            }
        )
        line = self.env["sale.order.line"].create(
            {
                "order_id": order.id,
                "product_id": self.product_technical_a.product_variant_id.id,
                "product_uom_qty": 2.0,
                "dipl_development_mm": 100.0,
                "dipl_width_mm": 50.0,
                "name": "Tech line formula pricelist",
            }
        )
        self.assertEqual(line.pricelist_item_id, rule)
        self.assertAlmostEqual(line.dipl_technical_price_unit, 4.71, places=2)
        self.assertAlmostEqual(line.price_unit, 5.739, places=3)
        self.assertAlmostEqual(line.technical_price_unit, 5.739, places=3)
        self.assertEqual(line.discount, 0.0)
        self.assertEqual(line.dipl_pricing_state, "pricelist_adjusted")

    def test_fixed_pricelist_rule_is_ignored_for_technical_lines(self):
        pricelist = self._create_pricelist("Tech Fixed")
        self.env["product.pricelist.item"].create(
            {
                "pricelist_id": pricelist.id,
                "applied_on": "1_product",
                "product_tmpl_id": self.product_technical_a.id,
                "compute_price": "fixed",
                "fixed_price": 99.0,
            }
        )
        order = self.env["sale.order"].create(
            {
                "partner_id": self.partner.id,
                "pricelist_id": pricelist.id,
            }
        )
        line = self.env["sale.order.line"].create(
            {
                "order_id": order.id,
                "product_id": self.product_technical_a.product_variant_id.id,
                "product_uom_qty": 2.0,
                "dipl_development_mm": 100.0,
                "dipl_width_mm": 50.0,
                "name": "Tech line fixed pricelist",
            }
        )
        self.assertFalse(line.pricelist_item_id)
        self.assertAlmostEqual(
            line.price_unit, line.dipl_technical_price_unit, places=4
        )
        self.assertEqual(line.dipl_pricing_state, "technical")

    def test_manual_final_price_is_reset_on_technical_change(self):
        pricelist = self._create_pricelist("Tech Formula Keep Manual")
        self.env["product.pricelist.item"].create(
            {
                "pricelist_id": pricelist.id,
                "applied_on": "1_product",
                "product_tmpl_id": self.product_technical_a.id,
                "compute_price": "formula",
                "base": "list_price",
                "price_discount": 10.0,
                "price_surcharge": 1.5,
            }
        )
        order = self.env["sale.order"].create(
            {
                "partner_id": self.partner.id,
                "pricelist_id": pricelist.id,
            }
        )
        line = self.env["sale.order.line"].create(
            {
                "order_id": order.id,
                "product_id": self.product_technical_a.product_variant_id.id,
                "product_uom_qty": 2.0,
                "dipl_development_mm": 100.0,
                "dipl_width_mm": 50.0,
                "name": "Tech line manual final",
            }
        )
        computed_price = line.price_unit
        line.write({"price_unit": 123.45})
        self.assertTrue(line.dipl_has_manual_final_price)
        self.assertEqual(line.dipl_pricing_state, "manual_final")
        line.write({"dipl_width_mm": 100.0})
        self.assertFalse(line.dipl_has_manual_final_price)
        self.assertNotAlmostEqual(line.price_unit, 123.45, places=2)
        self.assertNotAlmostEqual(line.price_unit, computed_price, places=2)
        self.assertEqual(line.dipl_pricing_state, "pricelist_adjusted")

    def test_manual_final_price_is_reset_on_quantity_change(self):
        line = self._create_geometry_line(name="Tech line manual final reset quantity")
        line.write({"price_unit": 123.45})
        self.assertTrue(line.dipl_has_manual_final_price)
        line.write({"product_uom_qty": 4.0})
        self.assertFalse(line.dipl_has_manual_final_price)
        self.assertNotAlmostEqual(line.price_unit, 123.45, places=2)
        self.assertEqual(line.dipl_pricing_state, "technical")

    def test_manual_final_price_is_reset_on_product_change(self):
        line = self._create_geometry_line(name="Tech line manual final reset product")
        line.write({"price_unit": 123.45})
        self.assertTrue(line.dipl_has_manual_final_price)
        line.write({"product_id": self.product_technical_b.product_variant_id.id})
        self.assertFalse(line.dipl_has_manual_final_price)
        self.assertAlmostEqual(line.price_unit, 8.15, places=2)
        self.assertEqual(line.dipl_pricing_state, "technical")

    def test_update_prices_clears_manual_final_price(self):
        pricelist = self._create_pricelist("Tech Formula Update Prices")
        self.env["product.pricelist.item"].create(
            {
                "pricelist_id": pricelist.id,
                "applied_on": "1_product",
                "product_tmpl_id": self.product_technical_a.id,
                "compute_price": "formula",
                "base": "list_price",
                "price_discount": 10.0,
                "price_surcharge": 1.5,
            }
        )
        order = self.env["sale.order"].create(
            {
                "partner_id": self.partner.id,
                "pricelist_id": pricelist.id,
            }
        )
        line = self.env["sale.order.line"].create(
            {
                "order_id": order.id,
                "product_id": self.product_technical_a.product_variant_id.id,
                "product_uom_qty": 2.0,
                "dipl_development_mm": 100.0,
                "dipl_width_mm": 50.0,
                "name": "Tech line update prices clears manual final",
            }
        )
        line.write({"price_unit": 123.45})
        self.assertTrue(line.dipl_has_manual_final_price)
        order.action_update_prices()
        line.invalidate_recordset(
            [
                "price_unit",
                "technical_price_unit",
                "dipl_pricing_state",
                "dipl_has_manual_final_price",
            ]
        )
        self.assertFalse(line.dipl_has_manual_final_price)
        self.assertNotAlmostEqual(line.price_unit, 123.45, places=2)
        self.assertEqual(line.dipl_pricing_state, "pricelist_adjusted")

    def test_pricelist_change_does_not_recompute_technical_lines_until_update_prices(self):
        pricelist_a = self._create_pricelist("Tech Formula A")
        self.env["product.pricelist.item"].create(
            {
                "pricelist_id": pricelist_a.id,
                "applied_on": "1_product",
                "product_tmpl_id": self.product_technical_a.id,
                "compute_price": "formula",
                "base": "list_price",
                "price_discount": 10.0,
                "price_surcharge": 1.5,
            }
        )
        pricelist_b = self._create_pricelist("Tech Formula B")
        self.env["product.pricelist.item"].create(
            {
                "pricelist_id": pricelist_b.id,
                "applied_on": "1_product",
                "product_tmpl_id": self.product_technical_a.id,
                "compute_price": "formula",
                "base": "list_price",
                "price_discount": 20.0,
                "price_surcharge": 3.0,
            }
        )
        order = self.env["sale.order"].create(
            {
                "partner_id": self.partner.id,
                "pricelist_id": pricelist_a.id,
            }
        )
        line = self.env["sale.order.line"].create(
            {
                "order_id": order.id,
                "product_id": self.product_technical_a.product_variant_id.id,
                "product_uom_qty": 2.0,
                "dipl_development_mm": 100.0,
                "dipl_width_mm": 50.0,
                "name": "Tech line pricelist change",
            }
        )
        original_price_unit = line.price_unit
        order.write({"pricelist_id": pricelist_b.id})
        line.invalidate_recordset(
            [
                "price_unit",
                "technical_price_unit",
                "pricelist_item_id",
                "dipl_pricing_state",
            ]
        )
        self.assertAlmostEqual(line.price_unit, original_price_unit, places=4)
        self.assertEqual(line.dipl_pricing_state, "pricelist_adjusted")
        order.action_update_prices()
        line.invalidate_recordset(
            [
                "price_unit",
                "technical_price_unit",
                "pricelist_item_id",
                "dipl_pricing_state",
            ]
        )
        self.assertNotAlmostEqual(line.price_unit, original_price_unit, places=4)
        self.assertEqual(line.dipl_pricing_state, "pricelist_adjusted")
