# -*- coding: utf-8 -*-

{
    "name": "Dipleg Sales Internal Documents",
    "summary": "Internal cutting and administrative sales documents",
    "version": "19.0.1.1.3",
    "category": "Dipleg",
    "license": "LGPL-3",
    "author": "Dipleg",
    "depends": [
        "sale_management",
        "dipl_doc_sale",
        "dipl_sale_technical_quote",
        "l10n_ar",
    ],
    "data": [
        "report/internal_document_actions.xml",
        "report/commercial_document_extensions.xml",
        "report/internal_document_templates.xml",
        "views/sale_order_views.xml",
    ],
    "installable": True,
    "application": False,
}
