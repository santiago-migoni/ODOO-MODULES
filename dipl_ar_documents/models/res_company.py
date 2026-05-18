from odoo import models


class ResCompany(models.Model):
    _inherit = "res.company"

    def _dipl_ar_documents_is_active(self):
        self.ensure_one()
        fiscal_country = self.account_fiscal_country_id or self.country_id
        return fiscal_country.code == "AR"
