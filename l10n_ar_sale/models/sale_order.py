from odoo import models


class SaleOrder(models.Model):
    _inherit = "sale.order"

    def _get_name_sale_report(self, report_xml_id):
        """Return localized sale report template xmlid for AR companies."""
        self.ensure_one()

        if self.company_id.country_id.code != "AR":
            return report_xml_id

        report_map = {
            "sale.report_saleorder_document": "l10n_ar_sale.report_saleorder_document",
        }
        return report_map.get(report_xml_id, report_xml_id)
