from odoo.tests.common import TransactionCase


class TestDiplArDocumentsInstall(TransactionCase):
    def test_helpers_model_is_registered(self):
        self.env["dipl.ar.document.helpers"]

    def test_company_activation_uses_fiscal_country(self):
        company = self.env.company
        company.account_fiscal_country_id = self.env.ref("base.ar")
        self.assertTrue(company._dipl_ar_documents_is_active())

    def test_helper_field_render_policy(self):
        helpers = self.env["dipl.ar.document.helpers"]
        self.assertFalse(helpers._dipl_ar_should_render_field(""))
        self.assertFalse(helpers._dipl_ar_should_render_field("   "))
        self.assertTrue(helpers._dipl_ar_should_render_field("x"))

    def test_partner_tax_data_rejects_generic_identification(self):
        identification_type = self.env["l10n_latam.identification.type"].create({
            "name": "Sigd",
            "country_id": self.env.ref("base.ar").id,
        })
        partner = self.env["res.partner"].create({
            "name": "Test Partner",
            "vat": "30717138151",
            "l10n_latam_identification_type_id": identification_type.id,
        })
        helpers = self.env["dipl.ar.document.helpers"]
        self.assertFalse(helpers._dipl_ar_has_partner_tax_data(partner))

    def test_partner_tax_label_prefers_identification_type_name(self):
        helpers = self.env["dipl.ar.document.helpers"]
        identification_type = self.env["l10n_latam.identification.type"].create({
            "name": "CUIT",
            "country_id": self.env.ref("base.ar").id,
        })
        partner = self.env["res.partner"].create({
            "name": "Test Partner",
            "vat": "30717138151",
            "l10n_latam_identification_type_id": identification_type.id,
        })

        self.assertEqual(
            helpers._dipl_ar_get_partner_tax_label(partner, self.env.company),
            "CUIT",
        )
