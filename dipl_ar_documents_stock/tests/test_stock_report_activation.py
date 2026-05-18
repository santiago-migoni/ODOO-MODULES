from odoo.tests.common import TransactionCase


class TestDiplArDocumentsStockActivation(TransactionCase):
    def test_stock_adapter_activation_requires_ar_company(self):
        company = self.env.company
        company.account_fiscal_country_id = self.env.ref("base.ar")
        picking = self.env["stock.picking"].new({"company_id": company.id})

        self.assertTrue(picking._dipl_ar_documents_stock_is_active())

    def test_stock_adapter_exposes_titles_by_operation_type(self):
        company = self.env.company
        company.account_fiscal_country_id = self.env.ref("base.ar")
        warehouse = self.env["stock.warehouse"].search([("company_id", "=", company.id)], limit=1)
        picking = self.env["stock.picking"].new({
            "company_id": company.id,
            "picking_type_id": warehouse.in_type_id.id,
        })

        self.assertEqual(picking._dipl_ar_get_stock_report_title(), "Goods Receipt Note")
        self.assertEqual(picking._dipl_ar_get_stock_partner_label(), "Vendor")

    def test_stock_adapter_activation_rejects_non_ar_company(self):
        company = self.env.company
        company.account_fiscal_country_id = self.env.ref("base.us")
        picking = self.env["stock.picking"].new({"company_id": company.id})

        self.assertFalse(picking._dipl_ar_documents_stock_is_active())
