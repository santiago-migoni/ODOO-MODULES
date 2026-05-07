from odoo import api, fields, models


class SaleOrderLine(models.Model):
    _inherit = "sale.order.line"

    _DIPL_CRITICAL_SNAPSHOT_FIELDS = (
        "dipl_theoretical_kg",
        "dipl_price_per_kg",
    )
    _DIPL_FINAL_PRICE_RESET_TRIGGER_FIELDS = (
        "product_id",
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
    dipl_theoretical_kg = fields.Float(
        string="Theoretical Kilograms",
        digits=(16, 4),
    )
    dipl_price_per_kg = fields.Monetary(
        string="Technical Price",
        currency_field="currency_id",
    )
    dipl_kg_total = fields.Float(
        string="Technical Kilograms",
        digits=(16, 4),
        compute="_compute_dipl_kg_values",
        store=True,
    )
    dipl_kg_mode = fields.Selection(
        selection=[
            ("geometry", "Geometry"),
            ("incomplete", "Incomplete"),
        ],
        string="Kg Mode",
        compute="_compute_dipl_kg_mode",
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
                "kg_total": 0.0,
                "technical_total": 0.0,
                "technical_price_unit": 0.0,
            }

        kg_mode = self._dipl_get_kg_mode()
        kg_total = 0.0
        if (
            kg_mode == "geometry"
            and self.product_uom_qty > 0
            and self.dipl_theoretical_kg > 0
        ):
            kg_total = (
                self.dipl_theoretical_kg
                * self.dipl_development_mm
                * self.dipl_width_mm
                * self.product_uom_qty
                / 1000000.0
            )

        technical_total = 0.0
        technical_price_unit = 0.0
        if self.product_uom_qty > 0:
            technical_total = kg_total * self.dipl_price_per_kg
            technical_price_unit = technical_total / self.product_uom_qty

        return {
            "kg_total": kg_total,
            "technical_total": technical_total,
            "technical_price_unit": technical_price_unit,
        }

    @api.model
    def _dipl_resolve_kg_mode(self, is_technical_line, development_mm, width_mm):
        if not is_technical_line:
            return False
        if development_mm > 0 and width_mm > 0:
            return "geometry"
        return "incomplete"

    def _dipl_get_kg_mode(self, extra_vals=None):
        self.ensure_one()
        extra_vals = extra_vals or {}
        return self._dipl_resolve_kg_mode(
            extra_vals.get("dipl_is_technical_line", self.dipl_is_technical_line),
            extra_vals.get("dipl_development_mm", self.dipl_development_mm),
            extra_vals.get("dipl_width_mm", self.dipl_width_mm),
        )

    @api.depends("dipl_is_technical_line", "dipl_development_mm", "dipl_width_mm")
    def _compute_dipl_kg_mode(self):
        for line in self:
            line.dipl_kg_mode = line._dipl_resolve_kg_mode(
                line.dipl_is_technical_line,
                line.dipl_development_mm,
                line.dipl_width_mm,
            )

    def _dipl_can_compute_technical_pricing(self):
        self.ensure_one()
        return bool(
            self.dipl_is_technical_line
            and self._dipl_get_kg_mode() == "geometry"
            and self.product_uom_qty > 0
            and self.dipl_price_per_kg >= 0
            and self.dipl_theoretical_kg > 0
        )

    @api.depends(
        "dipl_is_technical_line",
        "product_uom_qty",
        "dipl_development_mm",
        "dipl_width_mm",
        "dipl_theoretical_kg",
    )
    def _compute_dipl_kg_values(self):
        for line in self:
            if not line.dipl_is_technical_line:
                line.dipl_kg_total = 0.0
                continue

            technical_base = line._dipl_compute_technical_base()
            line.dipl_kg_total = technical_base["kg_total"]

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
        "product_uom_qty",
        "dipl_development_mm",
        "dipl_width_mm",
        "dipl_theoretical_kg",
        "dipl_price_per_kg",
        "dipl_technical_price_unit",
        "technical_price_unit",
        "price_unit",
        "pricelist_item_id",
        "discount",
    )
    def _compute_dipl_pricing_state(self):
        for line in self:
            if not line.dipl_is_technical_line:
                line.dipl_pricing_state = False
                continue

            has_manual_final_price = bool(
                line._dipl_uses_technical_pricing()
                and line._dipl_compare_amounts(
                    line.technical_price_unit, line.price_unit
                )
            )
            if has_manual_final_price:
                line.dipl_pricing_state = "manual_final"
            elif not line._dipl_can_compute_technical_pricing():
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
        "dipl_development_mm",
        "dipl_width_mm",
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
            "dipl_theoretical_kg": product_tmpl.dipl_theoretical_kg,
            "dipl_price_per_kg": product_tmpl.list_price,
        }

    def _dipl_prepare_snapshot_clear_vals(self):
        return {
            "dipl_is_technical_line": False,
            "dipl_theoretical_kg": 0.0,
            "dipl_price_per_kg": 0.0,
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

    def _dipl_needs_manual_final_price_reset(self, extra_vals=None):
        self.ensure_one()
        extra_vals = extra_vals or {}
        if not self._dipl_uses_technical_pricing():
            return False
        return any(
            field_name in extra_vals
            for field_name in self._DIPL_FINAL_PRICE_RESET_TRIGGER_FIELDS
        )

    def _dipl_prepare_manual_final_price_reset_vals(self, vals):
        reset_vals = dict(vals)
        reset_vals.pop("price_unit", None)
        reset_vals.pop("technical_price_unit", None)
        return reset_vals

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
            snapshot_state["dipl_theoretical_kg"] <= 0
            or snapshot_state["dipl_price_per_kg"] < 0
        )

    def _dipl_needs_snapshot_rehydration(self, extra_vals=None):
        self.ensure_one()
        if not self._dipl_is_snapshot_rehydratable():
            return False

        snapshot_state = self._dipl_get_critical_snapshot_state(extra_vals=extra_vals)
        if snapshot_state["dipl_price_per_kg"] == 0.0:
            return bool(self.product_id.product_tmpl_id.list_price != 0.0) or (
                snapshot_state["dipl_theoretical_kg"] <= 0
            )
        return self._dipl_is_incomplete_snapshot_state(snapshot_state)

    def _dipl_is_valid_snapshot_value(self, field_name, value):
        if field_name == "dipl_theoretical_kg":
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
        if snapshot_state["dipl_theoretical_kg"] <= 0:
            vals["dipl_theoretical_kg"] = product_tmpl.dipl_theoretical_kg
        if snapshot_state["dipl_price_per_kg"] == 0.0 and product_tmpl.list_price != 0.0:
            vals["dipl_price_per_kg"] = product_tmpl.list_price
        return vals

    @api.onchange("product_id")
    def _onchange_dipl_product_snapshot(self):
        for line in self:
            if line.display_type:
                continue
            line.update(line._dipl_prepare_snapshot_vals(line.product_id))

    @api.model
    def _dipl_sanitize_technical_vals(self, vals):
        normalized_vals = dict(vals)
        normalized_vals.pop("dipl_kg_total", None)
        normalized_vals.pop("dipl_kg_manual", None)
        normalized_vals.pop("dipl_use_manual_kg", None)
        normalized_vals.pop("dipl_thickness_mm", None)
        normalized_vals.pop("dipl_material_density", None)
        return normalized_vals

    @api.model_create_multi
    def create(self, vals_list):
        prepared_vals_list = []
        product_model = self.env["product.product"]
        for vals in vals_list:
            new_vals = self._dipl_sanitize_technical_vals(vals)
            if "product_id" in new_vals:
                product = product_model.browse(new_vals["product_id"])
                snapshot_vals = self.env["sale.order.line"]._dipl_prepare_snapshot_vals(
                    product
                )
                new_vals.update(snapshot_vals)
            prepared_vals_list.append(new_vals)
        return super().create(prepared_vals_list)

    def write(self, vals):
        vals = self._dipl_sanitize_technical_vals(vals)

        if "product_id" not in vals:
            result = True
            for line in self:
                line_vals = line._dipl_protect_snapshot_vals(vals)
                force_recompute = line._dipl_needs_manual_final_price_reset(
                    extra_vals=line_vals
                )
                if force_recompute:
                    line_vals = line._dipl_prepare_manual_final_price_reset_vals(
                        line_vals
                    )
                result = result and super(
                    SaleOrderLine,
                    line.with_context(force_price_recomputation=force_recompute),
                ).write(line_vals)
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
            force_recompute = line._dipl_needs_manual_final_price_reset(
                extra_vals=line_vals
            )
            if force_recompute:
                line_vals = line._dipl_prepare_manual_final_price_reset_vals(line_vals)
            result = result and super(
                SaleOrderLine,
                line.with_context(force_price_recomputation=force_recompute),
            ).write(line_vals)
        return result
