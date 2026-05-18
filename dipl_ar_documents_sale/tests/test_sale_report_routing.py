from odoo.tests.common import TransactionCase


class TestDiplArDocumentsSaleRouting(TransactionCase):
    def test_ar_company_maps_sale_report(self):
        company = self.env.company
        company.account_fiscal_country_id = self.env.ref("base.ar")
        order = self.env["sale.order"].new({"company_id": company.id})

        self.assertEqual(
            order._dipl_get_localized_sale_report_name("sale.report_saleorder_document"),
            "dipl_ar_documents_sale.report_saleorder_document",
        )

    def test_non_ar_company_keeps_native_report(self):
        company = self.env.company
        company.account_fiscal_country_id = self.env.ref("base.us")
        order = self.env["sale.order"].new({"company_id": company.id})

        self.assertEqual(
            order._dipl_get_localized_sale_report_name("sale.report_saleorder_document"),
            "sale.report_saleorder_document",
        )

    def test_unsupported_xmlid_falls_back(self):
        company = self.env.company
        company.account_fiscal_country_id = self.env.ref("base.ar")
        order = self.env["sale.order"].new({"company_id": company.id})

        self.assertEqual(
            order._dipl_get_localized_sale_report_name("sale.unknown_report"),
            "sale.unknown_report",
        )
