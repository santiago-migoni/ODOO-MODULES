# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

{
    'name': 'Interfaz Visual de Aplicaciones',
    'category': 'Hidden',
    'version': '19.0.1',
    'depends': ['web', 'base_setup'],
    'auto_install': False,
    'data': [
        'views/webclient_templates.xml',
        'views/webclient_templates.xml',
    ],
    'assets': {
        'web._assets_primary_variables': [
            ('after', 'web/static/src/scss/primary_variables.scss', 'dipl_ui_app_interface/static/src/**/*.variables.scss'),
            ('before', 'web/static/src/scss/primary_variables.scss', 'dipl_ui_app_interface/static/src/scss/primary_variables.scss'),
        ],
        'web._assets_secondary_variables': [
            ('before', 'web/static/src/scss/secondary_variables.scss', 'dipl_ui_app_interface/static/src/scss/secondary_variables.scss'),
        ],
        'web._assets_backend_helpers': [
            ('before', 'web/static/src/scss/bootstrap_overridden.scss', 'dipl_ui_app_interface/static/src/scss/bootstrap_overridden.scss'),
        ],
        'web.assets_frontend': [
            'dipl_ui_app_interface/static/src/webclient/home_menu/home_menu_background.scss', # used by login page
            'dipl_ui_app_interface/static/src/webclient/navbar/navbar.scss',
        ],
        'web.assets_backend': [
            'dipl_ui_app_interface/static/src/webclient/**/*.scss',
            'dipl_ui_app_interface/static/src/views/**/*.scss',

            'dipl_ui_app_interface/static/src/core/**/*',
            'dipl_ui_app_interface/static/src/webclient/**/*.js',
            ('after', 'web/static/src/views/list/list_renderer.xml', 'dipl_ui_app_interface/static/src/views/list/list_renderer_desktop.xml'),
            'dipl_ui_app_interface/static/src/webclient/**/*.xml',
            'dipl_ui_app_interface/static/src/views/**/*.js',
            'dipl_ui_app_interface/static/src/views/**/*.xml',
            ('remove', 'dipl_ui_app_interface/static/src/views/pivot/**'),

            # Don't include dark mode files in light mode
            ('remove', 'dipl_ui_app_interface/static/src/**/*.dark.scss'),
        ],
        'web.assets_backend_lazy': [
            'dipl_ui_app_interface/static/src/views/pivot/**',
        ],
        'web.assets_backend_lazy_dark': [
            ('include', 'web.dark_mode_variables'),
            # web._assets_backend_helpers
            ('before', 'dipl_ui_app_interface/static/src/scss/bootstrap_overridden.scss', 'dipl_ui_app_interface/static/src/scss/bootstrap_overridden.dark.scss'),
            ('after', 'web/static/lib/bootstrap/scss/_functions.scss', 'dipl_ui_app_interface/static/src/scss/bs_functions_overridden.dark.scss'),
        ],
        'web.assets_web': [
            ('replace', 'web/static/src/main.js', 'dipl_ui_app_interface/static/src/main.js'),
        ],
        # ========= Dark Mode =========
        "web.dark_mode_variables": [
            # web._assets_primary_variables
            ('before', 'dipl_ui_app_interface/static/src/scss/primary_variables.scss', 'dipl_ui_app_interface/static/src/scss/primary_variables.dark.scss'),
            ('before', 'dipl_ui_app_interface/static/src/**/*.variables.scss', 'dipl_ui_app_interface/static/src/**/*.variables.dark.scss'),
            # web._assets_secondary_variables
            ('before', 'dipl_ui_app_interface/static/src/scss/secondary_variables.scss', 'dipl_ui_app_interface/static/src/scss/secondary_variables.dark.scss'),
        ],
        "web.assets_web_dark": [
            ('include', 'web.dark_mode_variables'),
            # web._assets_backend_helpers
            ('before', 'dipl_ui_app_interface/static/src/scss/bootstrap_overridden.scss', 'dipl_ui_app_interface/static/src/scss/bootstrap_overridden.dark.scss'),
            ('after', 'web/static/lib/bootstrap/scss/_functions.scss', 'dipl_ui_app_interface/static/src/scss/bs_functions_overridden.dark.scss'),
            # assets_backend
            'dipl_ui_app_interface/static/src/**/*.dark.scss',
        ],
    },
    'author': 'Dipleg S.A.',
    "images": ["static/description/img.png"],
    'license': 'LGPL-3',
}
