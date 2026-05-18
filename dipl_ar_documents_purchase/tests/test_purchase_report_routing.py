from odoo.tests.common import TransactionCase


class TestDiplArDocumentsPurchaseRouting(TransactionCase):
    def test_ar_company_maps_purchase_quotation_report(self):
        company = self.env.company
        company.account_fiscal_country_id = self.env.ref("base.ar")
        order = self.env["purchase.order"].new({"company_id": company.id})

        self.assertEqual(
            order._dipl_get_localized_purchase_report_name("purchase.report_purchasequotation_document"),
            "dipl_ar_documents_purchase.report_purchasequotation_document",
        )

    def test_ar_company_maps_purchase_order_report(self):
        company = self.env.company
        company.account_fiscal_country_id = self.env.ref("base.ar")
        order = self.env["purchase.order"].new({"company_id": company.id})

        self.assertEqual(
            order._dipl_get_localized_purchase_report_name("purchase.report_purchaseorder_document"),
            "dipl_ar_documents_purchase.report_purchaseorder_document",
        )

    def test_non_ar_company_keeps_native_report(self):
        company = self.env.company
        company.account_fiscal_country_id = self.env.ref("base.us")
        order = self.env["purchase.order"].new({"company_id": company.id})

        self.assertEqual(
            order._dipl_get_localized_purchase_report_name("purchase.report_purchaseorder_document"),
            "purchase.report_purchaseorder_document",
        )

    def test_unsupported_xmlid_falls_back(self):
        company = self.env.company
        company.account_fiscal_country_id = self.env.ref("base.ar")
        order = self.env["purchase.order"].new({"company_id": company.id})

        self.assertEqual(
            order._dipl_get_localized_purchase_report_name("purchase.unknown_report"),
            "purchase.unknown_report",
        )
