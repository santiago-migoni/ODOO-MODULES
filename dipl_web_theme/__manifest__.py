# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

{
    "name": "Enterprise Web Theme",
    "category": "Dipleg",
    "version": "19.0.1.0.0",
    "depends": ["web", "base_setup"],
    "auto_install": False,
    "data": [
        "views/webclient_templates.xml",
    ],
    "assets": {
        "web._assets_primary_variables": [
            (
                "after",
                "web/static/src/scss/primary_variables.scss",
                "dipl_web_theme/static/src/**/*.variables.scss",
            ),
            (
                "before",
                "web/static/src/scss/primary_variables.scss",
                "dipl_web_theme/static/src/scss/primary_variables.scss",
            ),
        ],
        "web._assets_secondary_variables": [
            (
                "before",
                "web/static/src/scss/secondary_variables.scss",
                "dipl_web_theme/static/src/scss/secondary_variables.scss",
            ),
        ],
        "web._assets_backend_helpers": [
            (
                "before",
                "web/static/src/scss/bootstrap_overridden.scss",
                "dipl_web_theme/static/src/scss/bootstrap_overridden.scss",
            ),
        ],
        "web.assets_frontend": [
            "dipl_web_theme/static/src/webclient/home_menu/home_menu_background.scss",  # used by login page
            "dipl_web_theme/static/src/webclient/navbar/navbar.scss",
        ],
        "web.assets_backend": [
            "dipl_web_theme/static/src/webclient/**/*.scss",
            "dipl_web_theme/static/src/views/**/*.scss",
            "dipl_web_theme/static/src/core/**/*",
            "dipl_web_theme/static/src/webclient/color_scheme/color_scheme_menu_items.js",
            "dipl_web_theme/static/src/webclient/color_scheme/color_scheme_service.js",
            "dipl_web_theme/static/src/webclient/webclient.js",
            "dipl_web_theme/static/src/webclient/home_menu/home_menu.js",
            "dipl_web_theme/static/src/webclient/home_menu/home_menu_service.js",
            "dipl_web_theme/static/src/webclient/navbar/navbar.js",
            "dipl_web_theme/static/src/webclient/share_url/share_url.js",
            "dipl_web_theme/static/src/webclient/share_url/burger_menu.js",
            (
                "after",
                "web/static/src/views/list/list_renderer.xml",
                "dipl_web_theme/static/src/views/list/list_renderer_desktop.xml",
            ),
            "dipl_web_theme/static/src/webclient/home_menu/home_menu.xml",
            "dipl_web_theme/static/src/webclient/navbar/navbar.xml",
            "dipl_web_theme/static/src/webclient/share_url/burger_menu.xml",
            "dipl_web_theme/static/src/views/list/list_renderer_desktop.js",
            "dipl_web_theme/static/src/views/view_components/group_config_menu_patch.js",
            ("remove", "dipl_web_theme/static/src/views/pivot/**"),
            # Don't include dark mode files in light mode
            ("remove", "dipl_web_theme/static/src/**/*.dark.scss"),
        ],
        "web.assets_backend_lazy": [
            "dipl_web_theme/static/src/views/pivot/**",
        ],
        "web.assets_backend_lazy_dark": [
            ("include", "web.dark_mode_variables"),
            # web._assets_backend_helpers
            (
                "before",
                "dipl_web_theme/static/src/scss/bootstrap_overridden.scss",
                "dipl_web_theme/static/src/scss/bootstrap_overridden.dark.scss",
            ),
            (
                "after",
                "web/static/lib/bootstrap/scss/_functions.scss",
                "dipl_web_theme/static/src/scss/bs_functions_overridden.dark.scss",
            ),
        ],
        # ========= Dark Mode =========
        "web.dark_mode_variables": [
            # web._assets_primary_variables
            (
                "before",
                "dipl_web_theme/static/src/scss/primary_variables.scss",
                "dipl_web_theme/static/src/scss/primary_variables.dark.scss",
            ),
            (
                "before",
                "dipl_web_theme/static/src/**/*.variables.scss",
                "dipl_web_theme/static/src/**/*.variables.dark.scss",
            ),
            # web._assets_secondary_variables
            (
                "before",
                "dipl_web_theme/static/src/scss/secondary_variables.scss",
                "dipl_web_theme/static/src/scss/secondary_variables.dark.scss",
            ),
        ],
        "web.assets_web_dark": [
            ("include", "web.dark_mode_variables"),
            # web._assets_backend_helpers
            (
                "before",
                "dipl_web_theme/static/src/scss/bootstrap_overridden.scss",
                "dipl_web_theme/static/src/scss/bootstrap_overridden.dark.scss",
            ),
            (
                "after",
                "web/static/lib/bootstrap/scss/_functions.scss",
                "dipl_web_theme/static/src/scss/bs_functions_overridden.dark.scss",
            ),
            # assets_backend
            "dipl_web_theme/static/src/**/*.dark.scss",
        ],
    },
    "author": "Agga, IdeaCode Academy",
    "images": ["static/description/img.png"],
    "license": "LGPL-3",
}
