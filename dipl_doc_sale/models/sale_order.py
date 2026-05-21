# -*- coding: utf-8 -*-

from odoo import models


class SaleOrder(models.Model):
    _inherit = "sale.order"

    def _get_name_dipl_doc_sale_report(self, report_xml_id):
        self.ensure_one()
        if self.company_id.country_id.code != "AR":
            return report_xml_id
        if self.state in ("draft", "sent"):
            return "dipl_doc_sale.report_salequotation_document"
        return "dipl_doc_sale.report_saleorder_document"
