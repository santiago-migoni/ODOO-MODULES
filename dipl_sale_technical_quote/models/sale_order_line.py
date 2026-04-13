from odoo import api, fields, models
from odoo.exceptions import ValidationError


class SaleOrderLine(models.Model):
    _inherit = "sale.order.line"

    dipl_is_technical_line = fields.Boolean(
        string="Technical Quote Line",
        default=False,
        help="Indicates that this sales line uses the technical quotation flow.",
    )
    dipl_development_mm = fields.Float(
        string="Development (mm)",
        digits=(16, 2),
    )
    dipl_width_mm = fields.Float(
        string="Width (mm)",
        digits=(16, 2),
    )
    dipl_material_code = fields.Selection(
        selection=[
            ("sae", "SAE"),
            ("galv", "Galvanizado"),
            ("aisi", "Inoxidable"),
            ("sem", "Semillado"),
        ],
        string="Material",
    )
    dipl_thickness_label = fields.Char(
        string="Thickness Label",
    )
    dipl_thickness_mm = fields.Float(
        string="Thickness (mm)",
        digits=(16, 4),
    )
    dipl_material_density = fields.Float(
        string="Material Density",
        digits=(16, 6),
    )
    dipl_price_per_kg = fields.Monetary(
        string="Technical Price per Kg",
        currency_field="currency_id",
    )
    dipl_use_manual_kg = fields.Boolean(
        string="Use Manual Kg",
        default=False,
        help="If enabled, the line uses manually entered kg instead of the computed kg.",
    )
    dipl_kg_computed = fields.Float(
        string="Computed Kg",
        digits=(16, 4),
        readonly=True,
        compute="_compute_dipl_kg_values",
        store=True,
    )
    dipl_kg_manual = fields.Float(
        string="Manual Kg",
        digits=(16, 4),
    )
    dipl_kg_total = fields.Float(
        string="Effective Kg",
        digits=(16, 4),
        readonly=True,
        compute="_compute_dipl_kg_values",
        store=True,
    )
    dipl_technical_total = fields.Monetary(
        string="Technical Total",
        currency_field="currency_id",
        readonly=True,
        compute="_compute_dipl_pricing_values",
        store=True,
    )
    dipl_technical_price_unit = fields.Monetary(
        string="Technical Unit Price",
        currency_field="currency_id",
        readonly=True,
        compute="_compute_dipl_pricing_values",
        store=True,
    )
    dipl_can_compute = fields.Boolean(
        string="Can Compute Technical Pricing",
        compute="_compute_dipl_can_compute",
        store=True,
    )

    def _dipl_compute_technical_base(self):
        self.ensure_one()
        if not self.dipl_is_technical_line:
            return {
                "computed_kg": 0.0,
                "effective_kg": 0.0,
                "technical_total": 0.0,
                "technical_price_unit": 0.0,
            }

        computed_kg = 0.0
        if (
            self.product_uom_qty > 0
            and self.dipl_development_mm > 0
            and self.dipl_width_mm > 0
            and self.dipl_thickness_mm > 0
            and self.dipl_material_density > 0
        ):
            computed_kg = (
                self.dipl_material_density
                * self.dipl_thickness_mm
                * self.dipl_development_mm
                * self.dipl_width_mm
                * self.product_uom_qty
                / 1000000.0
            )

        effective_kg = self.dipl_kg_manual if self.dipl_use_manual_kg else computed_kg
        technical_total = 0.0
        technical_price_unit = 0.0
        if self.product_uom_qty > 0:
            technical_total = effective_kg * self.dipl_price_per_kg
            technical_price_unit = technical_total / self.product_uom_qty

        return {
            "computed_kg": computed_kg,
            "effective_kg": effective_kg,
            "technical_total": technical_total,
            "technical_price_unit": technical_price_unit,
        }

    def _dipl_get_target_price_unit(self):
        self.ensure_one()
        if not self.dipl_is_technical_line or not self.dipl_can_compute:
            return 0.0
        # Slice 03 uses the technical base price directly. Slice 04 can refine
        # this helper to let pricelists adjust the technical base explicitly.
        return self.dipl_technical_price_unit

    def _dipl_apply_technical_price_unit(self):
        self.ensure_one()
        target_price_unit = self._dipl_get_target_price_unit()
        self.update({
            "price_unit": target_price_unit,
            "technical_price_unit": target_price_unit,
        })

    @api.depends(
        "dipl_is_technical_line",
        "product_uom_qty",
        "dipl_development_mm",
        "dipl_width_mm",
        "dipl_thickness_mm",
        "dipl_material_density",
        "dipl_price_per_kg",
        "dipl_use_manual_kg",
        "dipl_kg_manual",
    )
    def _compute_dipl_can_compute(self):
        for line in self:
            line.dipl_can_compute = bool(
                line.dipl_is_technical_line
                and line.product_uom_qty > 0
                and line.dipl_price_per_kg >= 0
                and (
                    (line.dipl_use_manual_kg and line.dipl_kg_manual > 0)
                    or (
                        not line.dipl_use_manual_kg
                        and line.dipl_development_mm > 0
                        and line.dipl_width_mm > 0
                        and line.dipl_thickness_mm > 0
                        and line.dipl_material_density > 0
                    )
                )
            )

    @api.depends(
        "dipl_is_technical_line",
        "product_uom_qty",
        "dipl_development_mm",
        "dipl_width_mm",
        "dipl_thickness_mm",
        "dipl_material_density",
        "dipl_use_manual_kg",
        "dipl_kg_manual",
    )
    def _compute_dipl_kg_values(self):
        for line in self:
            if not line.dipl_is_technical_line:
                line.dipl_kg_computed = 0.0
                line.dipl_kg_total = 0.0
                continue

            technical_base = line._dipl_compute_technical_base()
            line.dipl_kg_computed = technical_base["computed_kg"]
            line.dipl_kg_total = technical_base["effective_kg"]

    @api.depends(
        "dipl_is_technical_line",
        "product_uom_qty",
        "dipl_kg_total",
        "dipl_price_per_kg",
    )
    def _compute_dipl_pricing_values(self):
        for line in self:
            if not line.dipl_is_technical_line or line.product_uom_qty <= 0:
                line.dipl_technical_total = 0.0
                line.dipl_technical_price_unit = 0.0
                continue

            technical_base = line._dipl_compute_technical_base()
            line.dipl_technical_total = technical_base["technical_total"]
            line.dipl_technical_price_unit = technical_base["technical_price_unit"]

    @api.depends(
        "product_id",
        "product_uom_id",
        "product_uom_qty",
        "dipl_is_technical_line",
        "dipl_technical_price_unit",
        "dipl_can_compute",
    )
    def _compute_price_unit(self):
        technical_lines = self.filtered(
            lambda line: line.dipl_is_technical_line and not line.is_downpayment and not line._is_global_discount()
        )
        regular_lines = self - technical_lines

        super(SaleOrderLine, regular_lines)._compute_price_unit()

        for line in technical_lines:
            if (
                not line.order_id
                or line.qty_invoiced > 0
                or (line.product_id.expense_policy == "cost" and line.is_expense)
            ):
                continue
            line = line.with_context(sale_write_from_compute=True)
            if not line.product_uom_id or not line.product_id:
                line.price_unit = 0.0
                line.technical_price_unit = 0.0
            else:
                line._reset_price_unit()

    def _reset_price_unit(self):
        self.ensure_one()
        if not self.dipl_is_technical_line:
            return super()._reset_price_unit()
        return self._dipl_apply_technical_price_unit()

    @api.model
    def _dipl_get_product_template_for_snapshot(self, product):
        if not product:
            return self.env["product.template"]
        return product.product_tmpl_id

    def _dipl_prepare_snapshot_vals(self, product):
        product_tmpl = self._dipl_get_product_template_for_snapshot(product)
        if not product_tmpl or not product_tmpl.dipl_is_technical_quote_product:
            return self._dipl_prepare_snapshot_clear_vals()
        return {
            "dipl_is_technical_line": True,
            "dipl_material_code": product_tmpl.dipl_material_code,
            "dipl_thickness_label": product_tmpl.dipl_thickness_label,
            "dipl_thickness_mm": product_tmpl.dipl_thickness_mm,
            "dipl_material_density": product_tmpl.dipl_material_density,
            "dipl_price_per_kg": product_tmpl.dipl_price_per_kg,
            "dipl_use_manual_kg": False,
            "dipl_kg_manual": 0.0,
            "dipl_kg_computed": 0.0,
            "dipl_kg_total": 0.0,
            "dipl_technical_total": 0.0,
            "dipl_technical_price_unit": 0.0,
        }

    def _dipl_prepare_snapshot_clear_vals(self):
        return {
            "dipl_is_technical_line": False,
            "dipl_material_code": False,
            "dipl_thickness_label": False,
            "dipl_thickness_mm": 0.0,
            "dipl_material_density": 0.0,
            "dipl_price_per_kg": 0.0,
            "dipl_use_manual_kg": False,
            "dipl_kg_manual": 0.0,
            "dipl_kg_computed": 0.0,
            "dipl_kg_total": 0.0,
            "dipl_technical_total": 0.0,
            "dipl_technical_price_unit": 0.0,
        }

    @api.onchange("product_id")
    def _onchange_dipl_product_snapshot(self):
        for line in self:
            if line.display_type:
                continue
            line.update(line._dipl_prepare_snapshot_vals(line.product_id))

    @api.onchange("dipl_use_manual_kg")
    def _onchange_dipl_use_manual_kg(self):
        for line in self:
            if not line.dipl_use_manual_kg:
                line.dipl_kg_manual = 0.0

    @api.model_create_multi
    def create(self, vals_list):
        prepared_vals_list = []
        product_model = self.env["product.product"]
        for vals in vals_list:
            new_vals = dict(vals)
            if "product_id" in new_vals:
                product = product_model.browse(new_vals["product_id"])
                snapshot_vals = self.env["sale.order.line"]._dipl_prepare_snapshot_vals(product)
                new_vals.update(snapshot_vals)
                for preserved_key in ("dipl_use_manual_kg", "dipl_kg_manual"):
                    if preserved_key in vals:
                        new_vals[preserved_key] = vals[preserved_key]
            prepared_vals_list.append(new_vals)
        return super().create(prepared_vals_list)

    def write(self, vals):
        if vals.get("dipl_use_manual_kg") is False and "dipl_kg_manual" not in vals:
            vals = dict(vals)
            vals["dipl_kg_manual"] = 0.0

        if "product_id" not in vals:
            return super().write(vals)

        result = True
        product_model = self.env["product.product"]
        if vals.get("product_id"):
            product = product_model.browse(vals["product_id"])
            snapshot_vals = self._dipl_prepare_snapshot_vals(product)
        else:
            snapshot_vals = self._dipl_prepare_snapshot_clear_vals()

        for line in self:
            line_vals = dict(vals)
            if not line.display_type:
                line_vals.update(snapshot_vals)
            result = result and super(SaleOrderLine, line).write(line_vals)
        return result

    @api.constrains("dipl_use_manual_kg", "dipl_kg_manual", "dipl_is_technical_line")
    def _check_dipl_manual_kg(self):
        for line in self:
            if line.dipl_is_technical_line and line.dipl_use_manual_kg and line.dipl_kg_manual <= 0:
                raise ValidationError("Manual kg must be greater than zero when manual override is enabled.")
