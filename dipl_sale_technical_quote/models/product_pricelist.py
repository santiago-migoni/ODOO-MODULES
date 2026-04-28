from odoo import fields, models


class ProductPricelist(models.Model):
    _inherit = "product.pricelist"

    def _compute_price_rule(
        self, products, quantity, *, currency=None, uom=None, date=False, compute_price=True, **kwargs
    ):
        self and self.ensure_one()
        if not kwargs.get("dipl_is_technical_line"):
            return super()._compute_price_rule(
                products,
                quantity,
                currency=currency,
                uom=uom,
                date=date,
                compute_price=compute_price,
                **kwargs,
            )

        currency = currency or self.currency_id or self.env.company.currency_id
        currency.ensure_one()

        if not products:
            return {}

        if not date:
            date = fields.Datetime.now()

        rules = self._get_applicable_rules(products, date, **kwargs)

        results = {}
        for product in products:
            suitable_rule = self.env["product.pricelist.item"]

            product_uom = product.uom_id
            target_uom = uom or product_uom
            if target_uom != product_uom:
                qty_in_product_uom = target_uom._compute_quantity(
                    quantity, product_uom, raise_if_failure=False
                )
            else:
                qty_in_product_uom = quantity

            for rule in rules:
                if not rule._is_applicable_for(product, qty_in_product_uom):
                    continue
                if rule.compute_price == "fixed":
                    continue
                suitable_rule = rule
                break

            if compute_price:
                price = suitable_rule._compute_price(
                    product,
                    quantity,
                    target_uom,
                    date=date,
                    currency=currency,
                    **kwargs,
                )
            else:
                price = 0.0

            results[product.id] = (price, suitable_rule.id)

        return results
