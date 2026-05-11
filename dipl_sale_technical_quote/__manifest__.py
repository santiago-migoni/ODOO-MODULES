# -*- coding: utf-8 -*-

{
    "name": "Technical Sales Quotation",
    "summary": "Industrial technical quotation over Sales orders",
    "version": "19.0.1.3.1",
    "category": "Dipleg",
    "license": "LGPL-3",
    "author": "Dipleg",
    "depends": [
        "sale_management",
    ],
    "data": [
        "security/ir.model.access.csv",
        "views/product_template_views.xml",
        "views/sale_order_views.xml",
        "views/sale_order_line_views.xml",
        "report/sale_report_views.xml",
    ],
    "installable": True,
    "application": False,
}
