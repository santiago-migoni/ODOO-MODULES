from odoo import api, fields, models
from odoo.exceptions import ValidationError


class ProductTemplate(models.Model):
    _inherit = "product.template"

    dipl_is_technical_quote_product = fields.Boolean(
        string="Technical Quote Product",
        help="Enable industrial quotation behavior for this product.",
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
        help="Human-readable thickness label, for example 3/8 or SAE 18.",
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
    dipl_price_per_kg = fields.Monetary(
        string="Technical Price",
        currency_field="currency_id",
        help="Technical tariff per kg used as the quotation base.",
    )
    dipl_requires_dimensions = fields.Boolean(
        string="Requires Dimensions",
        default=True,
        help="If enabled, sales lines must provide geometry to compute kg.",
    )
    dipl_technical_notes = fields.Text(
        string="Technical Notes",
        help="Internal notes for technical quotation maintenance.",
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

    @api.constrains(
        "dipl_is_technical_quote_product",
        "dipl_thickness_mm",
        "dipl_material_density",
        "dipl_price_per_kg",
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
            if product.dipl_price_per_kg < 0:
                raise ValidationError("Technical price per kg cannot be negative.")
