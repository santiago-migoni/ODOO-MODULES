from odoo import models


class ProductPricelistItem(models.Model):
    _inherit = "product.pricelist.item"

    def _compute_base_price(self, product, quantity, uom, date, currency, **kwargs):
        technical_base_price = kwargs.get("dipl_technical_base_price")
        technical_base_currency = kwargs.get("dipl_technical_base_currency")
        if kwargs.get("dipl_is_technical_line") and technical_base_price is not None:
            rule_base = self.base or "list_price"
            if rule_base == "list_price":
                src_currency = technical_base_currency or currency
                if src_currency != currency:
                    technical_base_price = src_currency._convert(
                        technical_base_price,
                        currency,
                        self.env.company,
                        date,
                        round=False,
                    )
                return technical_base_price
        return super()._compute_base_price(product, quantity, uom, date, currency, **kwargs)

    def _compute_price(self, product, quantity, uom, date, currency=None, **kwargs):
        if kwargs.get("dipl_is_technical_line") and self and self.compute_price == "fixed":
            currency = currency or self.currency_id or self.env.company.currency_id
            return self._compute_base_price(product, quantity, uom, date, currency, **kwargs)
        return super()._compute_price(product, quantity, uom, date, currency=currency, **kwargs)
