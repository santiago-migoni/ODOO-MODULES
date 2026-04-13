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
        string="Thickness (mm)",
        digits=(16, 4),
    )
    dipl_material_density = fields.Float(
        string="Material Density",
        digits=(16, 6),
        help="Physical density used by the technical quotation formula.",
    )
    dipl_price_per_kg = fields.Monetary(
        string="Technical Price per Kg",
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

    @api.constrains(
        "dipl_is_technical_quote_product",
        "dipl_material_code",
        "dipl_thickness_mm",
        "dipl_material_density",
        "dipl_price_per_kg",
    )
    def _check_dipl_technical_quote_fields(self):
        for product in self:
            if not product.dipl_is_technical_quote_product:
                continue
            if not product.dipl_material_code:
                raise ValidationError("Technical quote products require a material.")
            if product.dipl_thickness_mm <= 0:
                raise ValidationError("Technical quote products require a thickness greater than zero.")
            if product.dipl_material_density <= 0:
                raise ValidationError("Technical quote products require a material density greater than zero.")
            if product.dipl_price_per_kg < 0:
                raise ValidationError("Technical price per kg cannot be negative.")
