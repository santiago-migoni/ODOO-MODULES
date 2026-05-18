from odoo import models


class SaleOrder(models.Model):
    _inherit = "sale.order"

    def _dipl_get_localized_sale_report_name(self, report_xml_id):
        self.ensure_one()
        if not self.company_id._dipl_ar_documents_is_active():
            return report_xml_id

        report_map = {
            "sale.report_saleorder_document": "dipl_ar_documents_sale.report_saleorder_document",
        }
        return report_map.get(report_xml_id, report_xml_id)
