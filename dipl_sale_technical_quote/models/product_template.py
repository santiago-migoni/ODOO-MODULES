from odoo import SUPERUSER_ID, api, fields, models
from odoo.exceptions import ValidationError


class ProductTemplate(models.Model):
    _inherit = "product.template"

    dipl_is_technical_quote_product = fields.Boolean(
        string="Technical Quote Product",
        help="Enable industrial quotation behavior for this product.",
    )
    dipl_thickness_mm = fields.Float(
        string="Thickness",
        digits=(16, 6),
    )
    dipl_material_density = fields.Float(
        string="Density",
        digits=(16, 6),
        help="Physical density used by the technical quotation formula.",
    )
    dipl_theoretical_kg = fields.Float(
        string="Theoretical Kilograms",
        digits=(16, 4),
        compute="_compute_dipl_theoretical_kg",
        store=True,
        help="Theoretical kilograms per square meter derived from density and thickness.",
    )

    @api.depends("dipl_thickness_mm", "dipl_material_density")
    def _compute_dipl_theoretical_kg(self):
        for product in self:
            if product.dipl_thickness_mm > 0 and product.dipl_material_density > 0:
                product.dipl_theoretical_kg = (
                    product.dipl_material_density * product.dipl_thickness_mm
                )
            else:
                product.dipl_theoretical_kg = 0.0

    def _dipl_is_technical_product(self):
        self.ensure_one()
        return bool(self.dipl_is_technical_quote_product)

    def init(self):
        self._cr.execute(
            """
            SELECT 1
              FROM information_schema.columns
             WHERE table_name = 'product_template'
               AND column_name = 'dipl_price_per_kg'
             LIMIT 1
            """
        )
        if not self._cr.fetchone():
            return

        env = api.Environment(self._cr, SUPERUSER_ID, {})
        param_key = "dipl_sale_technical_quote.list_price_backfill_done"
        if env["ir.config_parameter"].sudo().get_param(param_key):
            return

        self._cr.execute(
            """
            UPDATE product_template
               SET list_price = dipl_price_per_kg
             WHERE dipl_is_technical_quote_product = TRUE
               AND dipl_price_per_kg IS NOT NULL
            """
        )
        env["ir.config_parameter"].sudo().set_param(param_key, "1")

    @api.constrains(
        "dipl_is_technical_quote_product",
        "dipl_thickness_mm",
        "dipl_material_density",
        "list_price",
    )
    def _check_dipl_technical_quote_fields(self):
        for product in self:
            if not product._dipl_is_technical_product():
                continue
            if product.dipl_thickness_mm <= 0:
                raise ValidationError(
                    "Technical quote products require a thickness greater than zero."
                )
            if product.dipl_material_density <= 0:
                raise ValidationError(
                    "Technical quote products require a material density greater than zero."
                )
            if product.list_price < 0:
                raise ValidationError("Technical price per kg cannot be negative.")
