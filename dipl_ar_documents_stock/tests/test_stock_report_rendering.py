from odoo import Command
from odoo.tests.common import TransactionCase


class TestDiplArDocumentsStockRendering(TransactionCase):
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
            "name": "Cliente Remito",
            "vat": "30717138151",
            "street": "Belgrano 456",
            "city": "Mendoza",
            "country_id": cls.env.ref("base.ar").id,
            "l10n_latam_identification_type_id": cls.identification_type.id,
            "company_id": False,
        })
        cls.warehouse = cls.env["stock.warehouse"].search(
            [("company_id", "=", cls.company.id)],
            limit=1,
        )
        cls.vendor_location = cls.env.ref("stock.stock_location_suppliers")
        cls.customer_location = cls.env.ref("stock.stock_location_customers")
        cls.product = cls.env["product.product"].create({
            "name": "Producto remito",
            "list_price": 100.0,
        })
        cls.out_type = cls.warehouse.out_type_id
        cls.in_type = cls.warehouse.in_type_id

    def _create_picking(self, picking_type, source_location, destination_location):
        return self.env["stock.picking"].create({
            "company_id": self.company.id,
            "partner_id": self.partner.id,
            "picking_type_id": picking_type.id,
            "location_id": source_location.id,
            "location_dest_id": destination_location.id,
            "move_ids": [
                Command.create({
                    "name": self.product.name,
                    "product_id": self.product.id,
                    "product_uom_qty": 1.0,
                    "location_id": source_location.id,
                    "location_dest_id": destination_location.id,
                })
            ],
        })

    def test_stock_report_renders_dipleg_outgoing_template(self):
        picking = self._create_picking(
            self.out_type,
            self.warehouse.lot_stock_id,
            self.customer_location,
        )

        html, _format = self.env["ir.actions.report"]._render_qweb_html(
            "stock.action_report_delivery",
            [picking.id],
        )
        html = html.decode()

        self.assertIn("Delivery Note", html)
        self.assertIn("Customer:", html)
        self.assertIn("CUIT:", html)
        self.assertIn("Delivery Address", html)

    def test_stock_report_renders_dipleg_incoming_template(self):
        picking = self._create_picking(
            self.in_type,
            self.vendor_location,
            self.warehouse.lot_stock_id,
        )

        html, _format = self.env["ir.actions.report"]._render_qweb_html(
            "stock.action_report_delivery",
            [picking.id],
        )
        html = html.decode()

        self.assertIn("Goods Receipt Note", html)
        self.assertIn("Vendor", html)
        self.assertIn("Warehouse Address", html)

    def test_stock_return_slip_renders_with_dipleg_header(self):
        picking = self._create_picking(
            self.out_type,
            self.warehouse.lot_stock_id,
            self.customer_location,
        )

        html, _format = self.env["ir.actions.report"]._render_qweb_html(
            "stock.return_label_report",
            [picking.id],
        )
        html = html.decode()

        self.assertIn("Return Slip", html)
        self.assertIn("Invalid document as invoice", html)
