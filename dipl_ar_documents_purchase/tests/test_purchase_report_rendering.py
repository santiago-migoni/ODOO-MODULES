from odoo import Command, fields
from odoo.tests.common import TransactionCase


class TestDiplArDocumentsPurchaseRendering(TransactionCase):
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
            "name": "Proveedor AR",
            "vat": "30712345678",
            "street": "San Martin 123",
            "city": "Mendoza",
            "country_id": cls.env.ref("base.ar").id,
            "l10n_latam_identification_type_id": cls.identification_type.id,
            "company_id": False,
            "supplier_rank": 1,
        })
        cls.product = cls.env["product.product"].create({
            "name": "Insumo de prueba",
            "type": "service",
            "standard_price": 50.0,
        })

    def _create_purchase_order(self, state="draft"):
        order = self.env["purchase.order"].create({
            "company_id": self.company.id,
            "partner_id": self.partner.id,
            "order_line": [
                Command.create({
                    "name": self.product.name,
                    "product_id": self.product.id,
                    "product_qty": 1.0,
                    "price_unit": 50.0,
                    "product_uom": self.product.uom_po_id.id,
                    "date_planned": fields.Datetime.now(),
                })
            ],
        })
        if state == "purchase":
            order.write({
                "state": "purchase",
                "date_approve": fields.Datetime.now(),
            })
        return order

    def test_purchase_report_renders_dipleg_rfq_template(self):
        order = self._create_purchase_order()

        html, _format = self.env["ir.actions.report"]._render_qweb_html(
            "purchase.report_purchase_quotation",
            [order.id],
        )
        html = html.decode()

        self.assertIn("Request for Quotation", html)
        self.assertIn("Supplier:", html)
        self.assertIn("CUIT:", html)
        self.assertIn("Date due:", html)

    def test_purchase_report_renders_dipleg_purchase_order_template(self):
        order = self._create_purchase_order(state="purchase")

        html, _format = self.env["ir.actions.report"]._render_qweb_html(
            "purchase.action_report_purchase_order",
            [order.id],
        )
        html = html.decode()

        self.assertIn("Purchase Order", html)
        self.assertIn("Approve date:", html)
        self.assertIn("% VAT", html)
