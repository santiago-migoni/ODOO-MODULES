from odoo.tests.common import TransactionCase


class TestTechnicalQuoteSaleOrderLineSnapshot(TransactionCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.partner = cls.env["res.partner"].create({"name": "Snapshot Customer"})
        cls.product_technical_a = cls.env["product.template"].create({
            "name": "Tech Product A",
            "sale_ok": True,
            "dipl_is_technical_quote_product": True,
            "dipl_material_code": "sae",
            "dipl_thickness_label": "18",
            "dipl_thickness_mm": 1.2,
            "dipl_material_density": 7.85,
            "dipl_price_per_kg": 100.0,
        })
        cls.product_technical_b = cls.env["product.template"].create({
            "name": "Tech Product B",
            "sale_ok": True,
            "dipl_is_technical_quote_product": True,
            "dipl_material_code": "galv",
            "dipl_thickness_label": "16",
            "dipl_thickness_mm": 1.6,
            "dipl_material_density": 8.15,
            "dipl_price_per_kg": 125.0,
        })
        cls.product_standard = cls.env["product.template"].create({
            "name": "Standard Product",
            "sale_ok": True,
        })
        cls.order = cls.env["sale.order"].create({
            "partner_id": cls.partner.id,
        })

    def _create_pricelist(self, name, **extra_vals):
        vals = {
            "name": name,
            "currency_id": self.order.currency_id.id,
        }
        vals.update(extra_vals)
        return self.env["product.pricelist"].create(vals)

    def test_snapshot_is_copied_on_create(self):
        line = self.env["sale.order.line"].create({
            "order_id": self.order.id,
            "product_id": self.product_technical_a.product_variant_id.id,
            "product_uom_qty": 1.0,
            "name": "Tech line",
        })
        self.assertTrue(line.dipl_is_technical_line)
        self.assertEqual(line.dipl_material_code, "sae")
        self.assertEqual(line.dipl_thickness_label, "18")
        self.assertEqual(line.dipl_thickness_mm, 1.2)
        self.assertEqual(line.dipl_material_density, 7.85)
        self.assertEqual(line.dipl_price_per_kg, 100.0)

    def test_snapshot_is_replaced_when_product_changes(self):
        line = self.env["sale.order.line"].create({
            "order_id": self.order.id,
            "product_id": self.product_technical_a.product_variant_id.id,
            "product_uom_qty": 1.0,
            "dipl_development_mm": 100.0,
            "dipl_width_mm": 50.0,
            "name": "Tech line change",
        })
        line.write({
            "product_id": self.product_technical_b.product_variant_id.id,
        })
        self.assertTrue(line.dipl_is_technical_line)
        self.assertEqual(line.dipl_material_code, "galv")
        self.assertEqual(line.dipl_thickness_label, "16")
        self.assertEqual(line.dipl_thickness_mm, 1.6)
        self.assertEqual(line.dipl_material_density, 8.15)
        self.assertEqual(line.dipl_price_per_kg, 125.0)
        self.assertAlmostEqual(line.dipl_technical_price_unit, 8.15, places=2)
        self.assertAlmostEqual(line.price_unit, 8.15, places=2)

    def test_snapshot_is_cleared_when_switching_to_non_technical_product(self):
        line = self.env["sale.order.line"].create({
            "order_id": self.order.id,
            "product_id": self.product_technical_a.product_variant_id.id,
            "product_uom_qty": 1.0,
            "name": "Tech line clear",
        })
        line.write({
            "product_id": self.product_standard.product_variant_id.id,
        })
        self.assertFalse(line.dipl_is_technical_line)
        self.assertFalse(line.dipl_material_code)
        self.assertFalse(line.dipl_thickness_label)
        self.assertEqual(line.dipl_thickness_mm, 0.0)
        self.assertEqual(line.dipl_material_density, 0.0)
        self.assertEqual(line.dipl_price_per_kg, 0.0)

    def test_snapshot_is_not_resynced_after_product_update(self):
        line = self.env["sale.order.line"].create({
            "order_id": self.order.id,
            "product_id": self.product_technical_a.product_variant_id.id,
            "product_uom_qty": 1.0,
            "name": "Tech line frozen",
        })
        self.product_technical_a.write({"dipl_price_per_kg": 200.0})
        line.invalidate_recordset(["dipl_price_per_kg"])
        self.assertEqual(line.dipl_price_per_kg, 100.0)

    def test_theoretical_kilograms_are_computed_on_product(self):
        self.assertAlmostEqual(self.product_technical_a.dipl_theoretical_kg, 9.42, places=2)

    def test_computed_kg_is_used_by_default(self):
        line = self.env["sale.order.line"].create({
            "order_id": self.order.id,
            "product_id": self.product_technical_a.product_variant_id.id,
            "product_uom_qty": 2.0,
            "dipl_development_mm": 100.0,
            "dipl_width_mm": 50.0,
            "name": "Tech line computed kg",
        })
        self.assertAlmostEqual(line.dipl_kg_computed, 0.0942, places=4)
        self.assertFalse(line.dipl_use_manual_kg)
        self.assertAlmostEqual(line.dipl_kg_total, line.dipl_kg_computed, places=4)
        self.assertAlmostEqual(line.dipl_technical_total, 9.42, places=2)
        self.assertAlmostEqual(line.dipl_technical_price_unit, 4.71, places=2)
        self.assertAlmostEqual(line.price_unit, 4.71, places=2)
        self.assertAlmostEqual(line.technical_price_unit, 4.71, places=2)
        self.assertEqual(line.dipl_pricing_state, "technical")

    def test_manual_kg_override_replaces_effective_kg(self):
        line = self.env["sale.order.line"].create({
            "order_id": self.order.id,
            "product_id": self.product_technical_a.product_variant_id.id,
            "product_uom_qty": 2.0,
            "dipl_development_mm": 100.0,
            "dipl_width_mm": 50.0,
            "dipl_use_manual_kg": True,
            "dipl_kg_manual": 1.5,
            "name": "Tech line manual kg",
        })
        self.assertAlmostEqual(line.dipl_kg_computed, 0.0942, places=4)
        self.assertTrue(line.dipl_use_manual_kg)
        self.assertAlmostEqual(line.dipl_kg_total, 1.5, places=4)
        self.assertAlmostEqual(line.dipl_technical_total, 150.0, places=2)
        self.assertAlmostEqual(line.dipl_technical_price_unit, 75.0, places=2)
        self.assertAlmostEqual(line.price_unit, 75.0, places=2)
        self.assertAlmostEqual(line.technical_price_unit, 75.0, places=2)
        self.assertEqual(line.dipl_pricing_state, "technical")

    def test_editing_kilograms_directly_enables_manual_override(self):
        line = self.env["sale.order.line"].create({
            "order_id": self.order.id,
            "product_id": self.product_technical_a.product_variant_id.id,
            "product_uom_qty": 2.0,
            "dipl_development_mm": 100.0,
            "dipl_width_mm": 50.0,
            "name": "Tech line direct kilograms edit",
        })
        line.dipl_kg_total = 2.25
        self.assertTrue(line.dipl_use_manual_kg)
        self.assertAlmostEqual(line.dipl_kg_manual, 2.25, places=4)
        self.assertAlmostEqual(line.dipl_kg_total, 2.25, places=4)

    def test_disabling_manual_override_falls_back_to_computed_kg(self):
        line = self.env["sale.order.line"].create({
            "order_id": self.order.id,
            "product_id": self.product_technical_a.product_variant_id.id,
            "product_uom_qty": 2.0,
            "dipl_development_mm": 100.0,
            "dipl_width_mm": 50.0,
            "dipl_use_manual_kg": True,
            "dipl_kg_manual": 1.5,
            "name": "Tech line fallback kg",
        })
        line.write({"dipl_use_manual_kg": False})
        self.assertFalse(line.dipl_use_manual_kg)
        self.assertEqual(line.dipl_kg_manual, 0.0)
        self.assertAlmostEqual(line.dipl_kg_total, line.dipl_kg_computed, places=4)
        self.assertAlmostEqual(line.price_unit, line.dipl_technical_price_unit, places=4)

    def test_dimension_change_updates_computed_kg_but_preserves_manual_override(self):
        line = self.env["sale.order.line"].create({
            "order_id": self.order.id,
            "product_id": self.product_technical_a.product_variant_id.id,
            "product_uom_qty": 2.0,
            "dipl_development_mm": 100.0,
            "dipl_width_mm": 50.0,
            "dipl_use_manual_kg": True,
            "dipl_kg_manual": 2.0,
            "name": "Tech line preserve manual kg",
        })
        original_manual = line.dipl_kg_manual
        line.write({"dipl_width_mm": 100.0})
        self.assertAlmostEqual(line.dipl_kg_computed, 0.1884, places=4)
        self.assertEqual(line.dipl_kg_manual, original_manual)
        self.assertAlmostEqual(line.dipl_kg_total, original_manual, places=4)
        self.assertAlmostEqual(line.dipl_technical_total, 200.0, places=2)
        self.assertAlmostEqual(line.dipl_technical_price_unit, 100.0, places=2)
        self.assertAlmostEqual(line.price_unit, 100.0, places=2)

    def test_changing_line_price_per_kg_recomputes_native_price_unit(self):
        line = self.env["sale.order.line"].create({
            "order_id": self.order.id,
            "product_id": self.product_technical_a.product_variant_id.id,
            "product_uom_qty": 2.0,
            "dipl_development_mm": 100.0,
            "dipl_width_mm": 50.0,
            "name": "Tech line price per kg update",
        })
        line.write({"dipl_price_per_kg": 200.0})
        self.assertAlmostEqual(line.dipl_technical_total, 18.84, places=2)
        self.assertAlmostEqual(line.dipl_technical_price_unit, 9.42, places=2)
        self.assertAlmostEqual(line.price_unit, 9.42, places=2)
        self.assertAlmostEqual(line.technical_price_unit, 9.42, places=2)

    def test_non_technical_lines_keep_native_price_logic(self):
        self.product_standard.write({"list_price": 42.0})
        line = self.env["sale.order.line"].create({
            "order_id": self.order.id,
            "product_id": self.product_standard.product_variant_id.id,
            "product_uom_qty": 3.0,
            "name": "Standard line",
        })
        self.assertFalse(line.dipl_is_technical_line)
        self.assertAlmostEqual(line.price_unit, 42.0, places=2)
        self.assertAlmostEqual(line.technical_price_unit, 42.0, places=2)

    def test_discount_remains_usable_on_technical_lines(self):
        line = self.env["sale.order.line"].create({
            "order_id": self.order.id,
            "product_id": self.product_technical_a.product_variant_id.id,
            "product_uom_qty": 2.0,
            "dipl_development_mm": 100.0,
            "dipl_width_mm": 50.0,
            "name": "Tech line discount",
        })
        line.write({"discount": 10.0})
        self.assertEqual(line.discount, 10.0)
        self.assertAlmostEqual(line.price_unit, line.dipl_technical_price_unit, places=4)

    def test_incomplete_technical_line_resolves_pricing_to_zero(self):
        line = self.env["sale.order.line"].create({
            "order_id": self.order.id,
            "product_id": self.product_technical_a.product_variant_id.id,
            "product_uom_qty": 2.0,
            "name": "Incomplete technical line",
        })
        self.assertEqual(line.dipl_kg_computed, 0.0)
        self.assertEqual(line.dipl_kg_total, 0.0)
        self.assertEqual(line.dipl_technical_total, 0.0)
        self.assertEqual(line.dipl_technical_price_unit, 0.0)
        self.assertEqual(line.price_unit, 0.0)
        self.assertEqual(line.dipl_pricing_state, "incomplete")

    def test_percentage_pricelist_applies_over_technical_base(self):
        pricelist = self._create_pricelist("Tech %")
        rule = self.env["product.pricelist.item"].create({
            "pricelist_id": pricelist.id,
            "applied_on": "1_product",
            "product_tmpl_id": self.product_technical_a.id,
            "compute_price": "percentage",
            "percent_price": 10.0,
        })
        order = self.env["sale.order"].create({
            "partner_id": self.partner.id,
            "pricelist_id": pricelist.id,
        })
        line = self.env["sale.order.line"].create({
            "order_id": order.id,
            "product_id": self.product_technical_a.product_variant_id.id,
            "product_uom_qty": 2.0,
            "dipl_development_mm": 100.0,
            "dipl_width_mm": 50.0,
            "name": "Tech line percentage pricelist",
        })
        effective_unit_price = line.price_unit * (1 - (line.discount or 0.0) / 100.0)
        self.assertEqual(line.pricelist_item_id, rule)
        self.assertAlmostEqual(line.dipl_technical_price_unit, 4.71, places=2)
        self.assertAlmostEqual(effective_unit_price, 4.239, places=3)
        self.assertEqual(line.dipl_pricing_state, "pricelist_adjusted")

    def test_formula_pricelist_applies_over_technical_base(self):
        pricelist = self._create_pricelist("Tech Formula")
        rule = self.env["product.pricelist.item"].create({
            "pricelist_id": pricelist.id,
            "applied_on": "1_product",
            "product_tmpl_id": self.product_technical_a.id,
            "compute_price": "formula",
            "base": "list_price",
            "price_discount": 10.0,
            "price_surcharge": 1.5,
        })
        order = self.env["sale.order"].create({
            "partner_id": self.partner.id,
            "pricelist_id": pricelist.id,
        })
        line = self.env["sale.order.line"].create({
            "order_id": order.id,
            "product_id": self.product_technical_a.product_variant_id.id,
            "product_uom_qty": 2.0,
            "dipl_development_mm": 100.0,
            "dipl_width_mm": 50.0,
            "name": "Tech line formula pricelist",
        })
        self.assertEqual(line.pricelist_item_id, rule)
        self.assertAlmostEqual(line.dipl_technical_price_unit, 4.71, places=2)
        self.assertAlmostEqual(line.price_unit, 5.739, places=3)
        self.assertAlmostEqual(line.technical_price_unit, 5.739, places=3)
        self.assertEqual(line.discount, 0.0)
        self.assertEqual(line.dipl_pricing_state, "pricelist_adjusted")

    def test_fixed_pricelist_rule_is_ignored_for_technical_lines(self):
        pricelist = self._create_pricelist("Tech Fixed")
        self.env["product.pricelist.item"].create({
            "pricelist_id": pricelist.id,
            "applied_on": "1_product",
            "product_tmpl_id": self.product_technical_a.id,
            "compute_price": "fixed",
            "fixed_price": 99.0,
        })
        order = self.env["sale.order"].create({
            "partner_id": self.partner.id,
            "pricelist_id": pricelist.id,
        })
        line = self.env["sale.order.line"].create({
            "order_id": order.id,
            "product_id": self.product_technical_a.product_variant_id.id,
            "product_uom_qty": 2.0,
            "dipl_development_mm": 100.0,
            "dipl_width_mm": 50.0,
            "name": "Tech line fixed pricelist",
        })
        self.assertFalse(line.pricelist_item_id)
        self.assertAlmostEqual(line.price_unit, line.dipl_technical_price_unit, places=4)
        self.assertEqual(line.dipl_pricing_state, "technical")

    def test_manual_final_price_is_preserved_until_update_prices(self):
        pricelist = self._create_pricelist("Tech Formula Keep Manual")
        self.env["product.pricelist.item"].create({
            "pricelist_id": pricelist.id,
            "applied_on": "1_product",
            "product_tmpl_id": self.product_technical_a.id,
            "compute_price": "formula",
            "base": "list_price",
            "price_discount": 10.0,
            "price_surcharge": 1.5,
        })
        order = self.env["sale.order"].create({
            "partner_id": self.partner.id,
            "pricelist_id": pricelist.id,
        })
        line = self.env["sale.order.line"].create({
            "order_id": order.id,
            "product_id": self.product_technical_a.product_variant_id.id,
            "product_uom_qty": 2.0,
            "dipl_development_mm": 100.0,
            "dipl_width_mm": 50.0,
            "name": "Tech line manual final",
        })
        computed_price = line.price_unit
        line.write({"price_unit": 123.45})
        self.assertTrue(line.dipl_has_manual_final_price)
        self.assertEqual(line.dipl_pricing_state, "manual_final")
        line.write({"dipl_width_mm": 100.0})
        self.assertAlmostEqual(line.price_unit, 123.45, places=2)
        self.assertTrue(line.dipl_has_manual_final_price)
        order.action_update_prices()
        line.invalidate_recordset(["price_unit", "technical_price_unit", "dipl_pricing_state", "dipl_has_manual_final_price"])
        self.assertFalse(line.dipl_has_manual_final_price)
        self.assertNotAlmostEqual(line.price_unit, 123.45, places=2)
        self.assertNotAlmostEqual(line.price_unit, computed_price, places=2)
        self.assertEqual(line.dipl_pricing_state, "pricelist_adjusted")
