from odoo import fields, models


class SaleReport(models.Model):
    _inherit = "sale.report"

    dipl_kg_total = fields.Float(
        string="Technical Kilograms",
        readonly=True,
    )

    def _select_additional_fields(self):
        res = super()._select_additional_fields()
        res["dipl_kg_total"] = (
            "CASE WHEN l.product_id IS NOT NULL THEN SUM(l.dipl_kg_total) ELSE 0 END"
        )
        return res
