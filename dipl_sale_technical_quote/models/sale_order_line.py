from odoo import api, fields, models
from odoo.exceptions import ValidationError
from odoo.tools import float_compare


class SaleOrderLine(models.Model):
    _inherit = "sale.order.line"

    _DIPL_CRITICAL_SNAPSHOT_FIELDS = (
        "dipl_thickness_mm",
        "dipl_material_density",
        "dipl_price_per_kg",
    )
    _DIPL_MANUAL_RESET_TRIGGER_FIELDS = (
        "product_uom_qty",
        "dipl_development_mm",
        "dipl_width_mm",
    )

    dipl_is_technical_line = fields.Boolean(
        string="Technical Quote Line",
        default=False,
        help="Indicates that this sales line uses the technical quotation flow.",
    )
    dipl_development_mm = fields.Float(
        string="Flat Pattern",
        digits=(16, 2),
    )
    dipl_width_mm = fields.Float(
        string="Flat Length",
        digits=(16, 2),
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
        string="Technical Price",
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
        string="Kilograms",
        digits=(16, 4),
        readonly=False,
        compute="_compute_dipl_kg_values",
        inverse="_inverse_dipl_kg_total",
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
    dipl_has_manual_final_price = fields.Boolean(
        string="Has Manual Final Price",
        compute="_compute_dipl_pricing_state",
    )
    dipl_pricing_state = fields.Selection(
        selection=[
            ("incomplete", "Incomplete"),
            ("technical", "Technical"),
            ("pricelist_adjusted", "Pricelist Adjusted"),
            ("manual_final", "Manual Final Price"),
        ],
        string="Pricing State",
        compute="_compute_dipl_pricing_state",
    )

    def _dipl_get_amount_compare_currency(self):
        self.ensure_one()
        return (
            self.currency_id
            or self.company_id.currency_id
            or self.env.company.currency_id
        )

    def _dipl_compare_amounts(self, amount_a, amount_b):
        self.ensure_one()
        return self._dipl_get_amount_compare_currency().compare_amounts(
            amount_a, amount_b
        )

    def _dipl_is_reward_line(self):
        self.ensure_one()
        return "is_reward_line" in self._fields and self.is_reward_line

    def _dipl_uses_technical_pricing(self):
        self.ensure_one()
        return (
            self.dipl_is_technical_line
            and not self.display_type
            and not self.is_downpayment
            and not self._is_global_discount()
            and not self._dipl_is_reward_line()
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

    def _inverse_dipl_kg_total(self):
        for line in self:
            if not line.dipl_is_technical_line:
                continue
            if (
                line.dipl_kg_total <= 0
                or float_compare(
                    line.dipl_kg_total, line.dipl_kg_computed, precision_digits=4
                )
                == 0
            ):
                line.dipl_use_manual_kg = False
                line.dipl_kg_manual = 0.0
            else:
                line.dipl_use_manual_kg = True
                line.dipl_kg_manual = line.dipl_kg_total

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
        "dipl_is_technical_line",
        "dipl_can_compute",
        "dipl_technical_price_unit",
        "technical_price_unit",
        "price_unit",
        "pricelist_item_id",
        "discount",
    )
    def _compute_dipl_pricing_state(self):
        for line in self:
            if not line.dipl_is_technical_line:
                line.dipl_has_manual_final_price = False
                line.dipl_pricing_state = False
                continue

            line.dipl_has_manual_final_price = bool(
                line._dipl_uses_technical_pricing()
                and line._dipl_compare_amounts(
                    line.technical_price_unit, line.price_unit
                )
            )
            if line.dipl_has_manual_final_price:
                line.dipl_pricing_state = "manual_final"
            elif not line.dipl_can_compute:
                line.dipl_pricing_state = "incomplete"
            elif line.pricelist_item_id and (
                line.discount
                or line._dipl_compare_amounts(
                    line.technical_price_unit, line.dipl_technical_price_unit
                )
            ):
                line.dipl_pricing_state = "pricelist_adjusted"
            else:
                line.dipl_pricing_state = "technical"

    def _get_pricelist_kwargs(self):
        kwargs = super()._get_pricelist_kwargs()
        if self._dipl_uses_technical_pricing() and self.currency_id:
            kwargs.update(
                {
                    "dipl_is_technical_line": True,
                    "dipl_technical_base_price": self.dipl_technical_price_unit,
                    "dipl_technical_base_currency": self.currency_id,
                }
            )
        return kwargs

    @api.depends(
        "product_id",
        "product_uom_id",
        "product_uom_qty",
        "dipl_is_technical_line",
        "dipl_technical_price_unit",
        "dipl_can_compute",
        "dipl_development_mm",
        "dipl_width_mm",
        "dipl_use_manual_kg",
        "dipl_kg_manual",
        "dipl_price_per_kg",
    )
    def _compute_price_unit(self):
        def has_manual_price(line):
            return bool(
                line._dipl_compare_amounts(line.technical_price_unit, line.price_unit)
            )

        force_recompute = self.env.context.get("force_price_recomputation")
        technical_lines = self.filtered(
            lambda line: line._dipl_uses_technical_pricing()
        )
        regular_lines = self - technical_lines

        super(SaleOrderLine, regular_lines)._compute_price_unit()

        for line in technical_lines:
            if (
                not line.order_id
                or (not force_recompute and has_manual_price(line))
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
        if not self._dipl_uses_technical_pricing():
            return super()._reset_price_unit()

        line = self.with_company(self.company_id)
        price = line._get_display_price()
        product_taxes = line.product_id.taxes_id._filter_taxes_by_company(
            line.company_id
        )
        price_unit = line.product_id._get_tax_included_unit_price_from_price(
            price,
            product_taxes=product_taxes,
            fiscal_position=line.order_id.fiscal_position_id,
        )
        line.update(
            {
                "price_unit": price_unit,
                "technical_price_unit": price_unit,
            }
        )

    @api.model
    def _dipl_get_product_template_for_snapshot(self, product):
        if not product:
            return self.env["product.template"]
        return product.product_tmpl_id

    def _dipl_prepare_snapshot_vals(self, product):
        product_tmpl = self._dipl_get_product_template_for_snapshot(product)
        if not product_tmpl or not product_tmpl._dipl_is_technical_product():
            return self._dipl_prepare_snapshot_clear_vals()
        return {
            "dipl_is_technical_line": True,
            "dipl_thickness_mm": product_tmpl.dipl_thickness_mm,
            "dipl_material_density": product_tmpl.dipl_material_density,
            "dipl_price_per_kg": product_tmpl.list_price,
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

    def _dipl_is_snapshot_rehydratable(self):
        self.ensure_one()
        if (
            not self.dipl_is_technical_line
            or not self.product_id
            or self.display_type
            or not self.product_id.product_tmpl_id._dipl_is_technical_product()
        ):
            return False
        return True

    def _dipl_prepare_manual_kg_reset_vals(self):
        return {
            "dipl_use_manual_kg": False,
            "dipl_kg_manual": 0.0,
        }

    def _dipl_needs_manual_kg_reset(self, extra_vals=None):
        self.ensure_one()
        extra_vals = extra_vals or {}
        if not self.dipl_is_technical_line or self.display_type:
            return False
        return any(
            field_name in extra_vals
            for field_name in self._DIPL_MANUAL_RESET_TRIGGER_FIELDS
        )

    def _dipl_get_critical_snapshot_state(self, extra_vals=None):
        self.ensure_one()
        extra_vals = extra_vals or {}
        state = {}
        for field_name in self._DIPL_CRITICAL_SNAPSHOT_FIELDS:
            if field_name in extra_vals:
                state[field_name] = extra_vals[field_name]
            else:
                state[field_name] = self[field_name]
        return state

    def _dipl_is_incomplete_snapshot_state(self, snapshot_state):
        return bool(
            snapshot_state["dipl_thickness_mm"] <= 0
            or snapshot_state["dipl_material_density"] <= 0
            or snapshot_state["dipl_price_per_kg"] < 0
        )

    def _dipl_needs_snapshot_rehydration(self, extra_vals=None):
        self.ensure_one()
        if not self._dipl_is_snapshot_rehydratable():
            return False

        snapshot_state = self._dipl_get_critical_snapshot_state(extra_vals=extra_vals)
        if snapshot_state["dipl_price_per_kg"] == 0.0:
            return bool(self.product_id.product_tmpl_id.list_price != 0.0) or (
                snapshot_state["dipl_thickness_mm"] <= 0
                or snapshot_state["dipl_material_density"] <= 0
            )
        return self._dipl_is_incomplete_snapshot_state(snapshot_state)

    def _dipl_is_valid_snapshot_value(self, field_name, value):
        if field_name in ("dipl_thickness_mm", "dipl_material_density"):
            return value and value > 0
        if field_name == "dipl_price_per_kg":
            return value is not False and value is not None and value > 0
        return bool(value)

    def _dipl_protect_snapshot_vals(self, vals):
        self.ensure_one()
        if not self._dipl_is_snapshot_rehydratable():
            return dict(vals)

        protected_vals = dict(vals)
        for field_name in self._DIPL_CRITICAL_SNAPSHOT_FIELDS:
            if (
                field_name in protected_vals
                and not self._dipl_is_valid_snapshot_value(
                    field_name, protected_vals[field_name]
                )
                and self._dipl_is_valid_snapshot_value(field_name, self[field_name])
            ):
                protected_vals[field_name] = self[field_name]

        if self._dipl_needs_snapshot_rehydration(extra_vals=protected_vals):
            protected_vals.update(
                self._dipl_prepare_missing_snapshot_vals(
                    self.product_id,
                    extra_vals=protected_vals,
                )
            )
        return protected_vals

    def _dipl_prepare_missing_snapshot_vals(self, product, extra_vals=None):
        self.ensure_one()
        extra_vals = extra_vals or {}
        product_tmpl = self._dipl_get_product_template_for_snapshot(product)
        if not product_tmpl or not product_tmpl._dipl_is_technical_product():
            return {}

        snapshot_state = self._dipl_get_critical_snapshot_state(extra_vals=extra_vals)
        vals = {}
        if snapshot_state["dipl_thickness_mm"] <= 0:
            vals["dipl_thickness_mm"] = product_tmpl.dipl_thickness_mm
        if snapshot_state["dipl_material_density"] <= 0:
            vals["dipl_material_density"] = product_tmpl.dipl_material_density
        if snapshot_state["dipl_price_per_kg"] == 0.0 and product_tmpl.list_price != 0.0:
            vals["dipl_price_per_kg"] = product_tmpl.list_price
        return vals

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

    @api.model
    def _dipl_normalize_manual_kg_payload(self, vals):
        normalized_vals = dict(vals)
        if (
            normalized_vals.get("dipl_use_manual_kg")
            and normalized_vals.get("dipl_kg_manual", 0.0) <= 0
        ):
            if normalized_vals.get("dipl_kg_total", 0.0) > 0:
                normalized_vals["dipl_kg_manual"] = normalized_vals["dipl_kg_total"]
            else:
                normalized_vals["dipl_use_manual_kg"] = False
                normalized_vals["dipl_kg_manual"] = 0.0
        elif (
            normalized_vals.get("dipl_use_manual_kg") is False
            and "dipl_kg_manual" not in normalized_vals
        ):
            normalized_vals["dipl_kg_manual"] = 0.0
        return normalized_vals

    @api.model_create_multi
    def create(self, vals_list):
        prepared_vals_list = []
        product_model = self.env["product.product"]
        for vals in vals_list:
            payload_vals = self._dipl_normalize_manual_kg_payload(vals)
            new_vals = dict(payload_vals)
            if "product_id" in payload_vals:
                product = product_model.browse(payload_vals["product_id"])
                snapshot_vals = self.env["sale.order.line"]._dipl_prepare_snapshot_vals(
                    product
                )
                new_vals.update(snapshot_vals)
                for preserved_key in ("dipl_use_manual_kg", "dipl_kg_manual"):
                    if preserved_key in payload_vals and (
                        payload_vals[preserved_key]
                        or payload_vals[preserved_key] == 0.0
                    ):
                        new_vals[preserved_key] = payload_vals[preserved_key]
            prepared_vals_list.append(new_vals)
        return super().create(prepared_vals_list)

    def write(self, vals):
        vals = self._dipl_normalize_manual_kg_payload(vals)

        if "product_id" not in vals:
            result = True
            for line in self:
                line_vals = line._dipl_protect_snapshot_vals(vals)
                if line._dipl_needs_manual_kg_reset(extra_vals=line_vals):
                    line_vals.pop("dipl_kg_total", None)
                    line_vals.update(line._dipl_prepare_manual_kg_reset_vals())
                result = result and super(SaleOrderLine, line).write(line_vals)
            return result

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
            if (
                line.dipl_is_technical_line
                and line.dipl_use_manual_kg
                and line.dipl_kg_manual <= 0
            ):
                raise ValidationError(
                    "Manual kg must be greater than zero when manual override is enabled."
                )
