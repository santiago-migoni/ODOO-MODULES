# -*- coding: utf-8 -*-
{
    "name": "Dipl UI Interface",
    "summary": "Interfaz moderna y responsiva basada en OWL 19",
    "version": "19.0.1.0.0",
    "category": "Hidden",
    "author": "Dipleg, BCA, IdeaCode Academy",
    "depends": ["web", "mail", "base_setup"],
    "license": "LGPL-3",
    "data": [
        "security/ir.model.access.csv",
        "views/webclient_templates.xml",
    ],
    "assets": {
        "web._assets_primary_variables": [
            ("after", "web/static/src/scss/primary_variables.scss", "dipl_ui_interface/static/src/**/*.variables.scss"),
            ("before", "web/static/src/scss/primary_variables.scss", "dipl_ui_interface/static/src/css_scss/primary_variables.scss"),
        ],
        "web._assets_secondary_variables": [
            ("before", "web/static/src/scss/secondary_variables.scss", "dipl_ui_interface/static/src/css_scss/secondary_variables.scss"),
        ],
        "web._assets_backend_helpers": [
            ("before", "web/static/src/scss/bootstrap_overridden.scss", "dipl_ui_interface/static/src/css_scss/bootstrap_overridden.scss"),
        ],
        "web.assets_frontend": [
            "dipl_ui_interface/static/src/webclient/home_menu/home_menu_background.scss",
            "dipl_ui_interface/static/src/webclient/navbar/navbar.scss",
        ],
        "web.assets_backend": [
            # Componentes Responsive (De dipl_ui_interface)
            "dipl_ui_interface/static/src/components/apps_menu_tools.esm.js",
            "dipl_ui_interface/static/src/components/apps_menu/*",
            "dipl_ui_interface/static/src/components/apps_menu_item/*",
            "dipl_ui_interface/static/src/components/chatter/*",
            "dipl_ui_interface/static/src/components/command_palette/*",
            
            # Estilos UI (De dipl_ui_interface)
            "dipl_ui_interface/static/src/webclient/**/*.scss",
            "dipl_ui_interface/static/src/webclient/**/*.js",
            "dipl_ui_interface/static/src/webclient/**/*.xml",
            
            # Remoción de oscuro (Modo claro por defecto)
            ("remove", "dipl_ui_interface/static/src/**/*.dark.scss"),
        ],
        "web.dark_mode_variables": [
            ("before", "dipl_ui_interface/static/src/css_scss/primary_variables.scss", "dipl_ui_interface/static/src/css_scss/primary_variables.dark.scss"),
            ("before", "dipl_ui_interface/static/src/**/*.variables.scss", "dipl_ui_interface/static/src/**/*.variables.dark.scss"),
            ("before", "dipl_ui_interface/static/src/css_scss/secondary_variables.scss", "dipl_ui_interface/static/src/css_scss/secondary_variables.dark.scss"),
        ],
        "web.assets_web_dark": [
            ("include", "web.dark_mode_variables"),
            ("before", "dipl_ui_interface/static/src/css_scss/bootstrap_overridden.scss", "dipl_ui_interface/static/src/css_scss/bootstrap_overridden.dark.scss"),
            ("after", "web/static/lib/bootstrap/scss/_functions.scss", "dipl_ui_interface/static/src/css_scss/bs_functions_overridden.dark.scss"),
            "dipl_ui_interface/static/src/**/*.dark.scss",
        ],
    },
    "installable": True,
    "application": False,
}