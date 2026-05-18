from odoo.tests.common import TransactionCase


class TestDiplArDocumentsPurchaseInstall(TransactionCase):
    def test_purchase_model_extension_is_available(self):
        self.env["purchase.order"]
