from odoo import Command
from odoo.tests.common import TransactionCase


class TestDiplArDocumentsSaleRendering(TransactionCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.company = cls.env.company
        cls.company.account_fiscal_country_id = cls.env.ref("base.ar")
        cls.identification_type = cls.env["l10n_latam.identification.type"].create({
            "name": "CUIT",
            "country_id": cls.env.ref("base.ar").id,
            "l10n_ar_afip_code": "80",
        })
        cls.partner = cls.env["res.partner"].create({
            "name": "Cliente AR",
            "vat": "30717138151",
            "street": "Av. Siempre Viva 742",
            "city": "Mendoza",
            "country_id": cls.env.ref("base.ar").id,
            "l10n_latam_identification_type_id": cls.identification_type.id,
            "company_id": False,
        })
        cls.product = cls.env["product.product"].create({
            "name": "Servicio de prueba",
            "type": "service",
            "list_price": 100.0,
        })

    def _create_sale_order(self, state="draft"):
        order = self.env["sale.order"].create({
            "company_id": self.company.id,
            "partner_id": self.partner.id,
            "order_line": [
                Command.create({
                    "name": self.product.name,
                    "product_id": self.product.id,
                    "product_uom_qty": 1.0,
                    "price_unit": 100.0,
                })
            ],
        })
        if state != "draft":
            order.write({"state": state})
        return order

    def test_sale_report_renders_dipleg_quotation_template(self):
        order = self._create_sale_order()

        html, _format = self.env["ir.actions.report"]._render_qweb_html(
            "sale.action_report_saleorder",
            [order.id],
        )
        html = html.decode()

        self.assertIn("Request for Quotation", html)
        self.assertIn("Customer:", html)
        self.assertIn("CUIT:", html)
        self.assertIn("Date due:", html)
        self.assertIn("Invalid document as invoice", html)

    def test_sale_report_renders_dipleg_sales_order_template(self):
        order = self._create_sale_order(state="sale")

        html, _format = self.env["ir.actions.report"]._render_qweb_html(
            "sale.action_report_saleorder",
            [order.id],
        )
        html = html.decode()

        self.assertIn("Sales Order", html)
        self.assertIn("Order date:", html)

    def test_sale_proforma_report_renders_dipleg_template(self):
        order = self._create_sale_order()

        html, _format = self.env["ir.actions.report"]._render_qweb_html(
            "sale.action_report_pro_forma_invoice",
            [order.id],
        )
        html = html.decode()

        self.assertIn("Pro-Forma Invoice", html)
        self.assertIn("Customer:", html)
