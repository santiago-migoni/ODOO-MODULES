from odoo.tests.common import TransactionCase


class TestDiplArDocumentsStockActivation(TransactionCase):
    def test_stock_adapter_activation_requires_ar_company(self):
        company = self.env.company
        company.account_fiscal_country_id = self.env.ref("base.ar")
        picking = self.env["stock.picking"].new({"company_id": company.id})
        picking.l10n_ar_delivery_guide_number = "00001-00000001"

        self.assertTrue(picking._dipl_ar_documents_stock_is_active())

    def test_stock_adapter_activation_requires_guide_number(self):
        company = self.env.company
        company.account_fiscal_country_id = self.env.ref("base.ar")
        picking = self.env["stock.picking"].new({"company_id": company.id})

        self.assertFalse(picking._dipl_ar_documents_stock_is_active())

    def test_stock_adapter_activation_rejects_non_ar_company(self):
        company = self.env.company
        company.account_fiscal_country_id = self.env.ref("base.us")
        picking = self.env["stock.picking"].new({"company_id": company.id})
        picking.l10n_ar_delivery_guide_number = "00001-00000001"

        self.assertFalse(picking._dipl_ar_documents_stock_is_active())
