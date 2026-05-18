from odoo.tests.common import TransactionCase


class TestDiplArDocumentsSaleInstall(TransactionCase):
    def test_sale_model_extension_is_available(self):
        self.env["sale.order"]
