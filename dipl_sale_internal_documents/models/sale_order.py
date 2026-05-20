# -*- coding: utf-8 -*-

from odoo import _, models
from odoo.exceptions import UserError


class SaleOrder(models.Model):
    _inherit = "sale.order"

    def _dipl_ensure_internal_document_printable(self):
        for order in self:
            if order.state != "sale":
                raise UserError(
                    _("Internal documents can only be printed from confirmed sales orders.")
                )

    def action_print_cutting_list(self):
        self.ensure_one()
        self._dipl_ensure_internal_document_printable()
        return self.env.ref(
            "dipl_sale_internal_documents.action_report_cutting_list"
        ).report_action(self)

    def action_print_internal_order(self):
        self.ensure_one()
        self._dipl_ensure_internal_document_printable()
        return self.env.ref(
            "dipl_sale_internal_documents.action_report_internal_sales_order"
        ).report_action(self)
