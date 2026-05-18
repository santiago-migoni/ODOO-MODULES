from odoo import models


class StockPicking(models.Model):
    _inherit = "stock.picking"

    def _dipl_ar_documents_stock_is_active(self):
        self.ensure_one()
        return self.company_id._dipl_ar_documents_is_active() and bool(self.l10n_ar_delivery_guide_number)
