from odoo import models


class DiplArDocumentHelpers(models.AbstractModel):
    _name = "dipl.ar.document.helpers"
    _description = "Dipleg AR document rendering helpers"

    def _dipl_ar_documents_enabled(self, company):
        return bool(company) and company._dipl_ar_documents_is_active()

    def _dipl_ar_should_render_field(self, value):
        if isinstance(value, str):
            return bool(value.strip())
        return bool(value)

    def _dipl_ar_has_partner_tax_data(self, partner):
        if not partner or not self._dipl_ar_should_render_field(partner.vat):
            return False

        identification_type = partner.l10n_latam_identification_type_id
        if not identification_type:
            return False

        afip_code = getattr(identification_type, "l10n_ar_afip_code", False)
        if afip_code == "99" or identification_type.name == "Sigd":
            return False

        return True

    def _dipl_ar_get_partner_tax_label(self, partner, company):
        identification_type = partner.l10n_latam_identification_type_id
        return identification_type.name or company.account_fiscal_country_id.vat_label or "Tax ID"

    def _dipl_ar_get_header_address(self, record):
        company = getattr(record, "company_id", False)
        return company.partner_id if company else False

    def _dipl_ar_get_document_identity_values(self, record):
        name = getattr(record, "name", False)
        report_date = getattr(record, "date_order", False) or getattr(record, "date", False)
        return {
            "report_number": name or "",
            "report_date": report_date or False,
        }

    def _dipl_ar_get_sale_report_title(self, order, is_proforma=False):
        if is_proforma:
            return "Pro-Forma Invoice"
        if order.state in ["draft", "sent"]:
            return "Request for Quotation"
        if order.state == "cancel":
            return "Cancelled Sales Order"
        return "Sales Order"

    def _dipl_ar_get_sale_report_date(self, order, is_proforma=False):
        if not is_proforma and order.state in ["draft", "sent"] and order.validity_date:
            return order.validity_date
        return order.date_order

    def _dipl_ar_get_purchase_report_title(self, order):
        if order.state in ["draft", "sent", "to approve"]:
            return "Request for Quotation"
        if order.state == "cancel":
            return "Cancelled Purchase Order"
        return "Purchase Order"

    def _dipl_ar_get_purchase_report_date(self, order):
        return order.date_approve or order.date_order
