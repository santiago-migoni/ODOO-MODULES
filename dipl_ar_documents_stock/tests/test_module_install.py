from odoo.tests.common import TransactionCase


class TestDiplArDocumentsStockInstall(TransactionCase):
    def test_stock_model_extension_is_available(self):
        self.env["stock.picking"]
