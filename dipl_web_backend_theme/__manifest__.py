{
    "name": "Dipleg Web Backend Theme",
    "version": "19.0.1.0.0",
    "summary": "Dipleg backend theme for Odoo Community",
    "category": "Hidden",
    "author": "Dipleg S.A.",
    "license": "LGPL-3",
    "depends": ["base", "web", "base_setup"],
    "data": [
        "views/webclient_templates.xml",
    ],
    "assets": {
        "web._assets_primary_variables": [
            (
                "before",
                "web/static/src/scss/primary_variables.scss",
                "dipl_web_backend_theme/static/src/scss/primary_variables.scss",
            ),
        ],
        "web._assets_secondary_variables": [
            (
                "before",
                "web/static/src/scss/secondary_variables.scss",
                "dipl_web_backend_theme/static/src/scss/secondary_variables.scss",
            ),
        ],
        "web._assets_backend_helpers": [
            (
                "before",
                "web/static/src/scss/bootstrap_overridden.scss",
                "dipl_web_backend_theme/static/src/scss/bootstrap_overridden.scss",
            ),
        ],
        "web.assets_backend": [
            "dipl_web_backend_theme/static/src/scss/backend.scss",
            "dipl_web_backend_theme/static/src/webclient/color_scheme/*.js",
            "dipl_web_backend_theme/static/src/webclient/home_menu/*.js",
            "dipl_web_backend_theme/static/src/webclient/home_menu/*.scss",
            "dipl_web_backend_theme/static/src/webclient/home_menu/*.xml",
            "dipl_web_backend_theme/static/src/webclient/navbar/*.js",
            "dipl_web_backend_theme/static/src/webclient/navbar/*.scss",
            "dipl_web_backend_theme/static/src/webclient/navbar/*.xml",
            "dipl_web_backend_theme/static/src/views/**/*.scss",
        ],
        "web.assets_frontend": [
            "dipl_web_backend_theme/static/src/scss/frontend.scss",
            "dipl_web_backend_theme/static/src/webclient/home_menu/home_menu_background.scss",
        ],
        "web.dark_mode_variables": [
            (
                "before",
                "dipl_web_backend_theme/static/src/scss/primary_variables.scss",
                "dipl_web_backend_theme/static/src/scss/primary_variables.dark.scss",
            ),
            (
                "before",
                "dipl_web_backend_theme/static/src/scss/secondary_variables.scss",
                "dipl_web_backend_theme/static/src/scss/secondary_variables.dark.scss",
            ),
        ],
        "web.assets_web_dark": [
            ("include", "web.dark_mode_variables"),
            "dipl_web_backend_theme/static/src/scss/backend.dark.scss",
            "dipl_web_backend_theme/static/src/webclient/home_menu/home_menu_background.dark.scss",
        ],
        "web.assets_backend_lazy_dark": [
            ("include", "web.dark_mode_variables"),
            (
                "before",
                "dipl_web_backend_theme/static/src/scss/bootstrap_overridden.scss",
                "dipl_web_backend_theme/static/src/scss/bootstrap_overridden.dark.scss",
            ),
        ],
    },
    "installable": True,
    "application": False,
}
