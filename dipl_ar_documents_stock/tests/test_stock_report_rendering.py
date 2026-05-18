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
        cls.customer_location = cls.env.ref("stock.stock_location_customers")
        cls.product = cls.env["product.product"].create({
            "name": "Producto remito",
            "list_price": 100.0,
        })
        cls.picking_type = cls.env["stock.picking.type"].create({
            "name": "Remito Dipleg",
            "code": "outgoing",
            "company_id": cls.company.id,
            "sequence_code": "OUT",
            "warehouse_id": cls.warehouse.id,
            "l10n_ar_document_type_id": cls.env.ref("l10n_ar.dc_r_r").id,
            "l10n_ar_cai_authorization_code": "1234567890",
            "l10n_ar_cai_expiration_date": "2026-12-31",
            "l10n_ar_sequence_number_start": "00000001",
            "l10n_ar_sequence_number_end": "00000999",
            "default_location_src_id": cls.warehouse.lot_stock_id.id,
            "default_location_dest_id": cls.customer_location.id,
        })

    def _create_done_picking(self):
        picking = self.env["stock.picking"].create({
            "company_id": self.company.id,
            "partner_id": self.partner.id,
            "picking_type_id": self.picking_type.id,
            "location_id": self.warehouse.lot_stock_id.id,
            "location_dest_id": self.customer_location.id,
            "move_ids": [
                Command.create({
                    "name": self.product.name,
                    "product_id": self.product.id,
                    "product_uom_qty": 1.0,
                    "location_id": self.warehouse.lot_stock_id.id,
                    "location_dest_id": self.customer_location.id,
                })
            ],
        })
        picking.action_confirm()
        picking.button_validate()
        picking.l10n_ar_action_create_delivery_guide()
        return picking

    def test_stock_report_renders_dipleg_delivery_guide_template(self):
        picking = self._create_done_picking()

        html, _format = self.env["ir.actions.report"]._render_qweb_html(
            "l10n_ar_stock.action_delivery_guide_report_pdf",
            [picking.id],
        )
        html = html.decode()

        self.assertIn("DOCUMENT NOT VALID AS AN INVOICE", html)
        self.assertIn("Delivery Guide No:", html)
        self.assertIn("Customer:", html)
        self.assertIn("CAI:", html)
