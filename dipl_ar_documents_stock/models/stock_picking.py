from odoo import _, models


class StockPicking(models.Model):
    _inherit = "stock.picking"

    def _dipl_ar_documents_stock_is_active(self):
        self.ensure_one()
        return self.company_id._dipl_ar_documents_is_active()

    def _dipl_ar_get_stock_report_title(self):
        self.ensure_one()
        return self.picking_type_id._get_code_report_name() or _("Transfer")

    def _dipl_ar_get_stock_partner_label(self):
        self.ensure_one()
        code = self.picking_type_id.code
        if code == "incoming":
            return _("Vendor")
        if code == "outgoing":
            return _("Customer")
        if code == "internal":
            return _("Contact")
        return _("Partner")

    def _dipl_ar_get_stock_address_label(self):
        self.ensure_one()
        code = self.picking_type_id.code
        if code == "outgoing":
            return _("Delivery Address")
        if code == "incoming":
            return _("Warehouse Address")
        if code == "internal":
            return _("Destination")
        return _("Address")

    def _dipl_ar_get_stock_address_partner(self):
        self.ensure_one()
        if self.should_print_delivery_address():
            return (self.move_ids and self.move_ids[0].partner_id) or self.partner_id
        if self.picking_type_id.code == "internal":
            return self.location_dest_id.warehouse_id.partner_id or self.picking_type_id.warehouse_id.partner_id
        return self.picking_type_id.warehouse_id.partner_id
