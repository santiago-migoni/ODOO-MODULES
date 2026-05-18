from odoo import models


class PurchaseOrder(models.Model):
    _inherit = "purchase.order"

    def _dipl_get_localized_purchase_report_name(self, report_xml_id):
        self.ensure_one()
        if not self.company_id._dipl_ar_documents_is_active():
            return report_xml_id

        report_map = {
            "purchase.report_purchasequotation_document": "dipl_ar_documents_purchase.report_purchasequotation_document",
            "purchase.report_purchaseorder_document": "dipl_ar_documents_purchase.report_purchaseorder_document",
        }
        return report_map.get(report_xml_id, report_xml_id)
