# -*- coding: utf-8 -*-
{
    'name': 'Dipleg Web UI Enhanced',
    'category': 'Hidden',
    'version': '1.0',
    'summary': 'Enhanced Responsive Web UI for Dipleg',
    'description': """
        Responsive Web Client for Dipleg based on Dipleg Enterprise layout.
        This module provides an enterprise-like experience for the community version.
    """,
    'depends': ['web', 'base_setup'],
    'auto_install': False,
    'data': [
        'views/webclient_templates.xml',
    ],
    'assets': {
        'web._assets_primary_variables': [
            ('after', 'web/static/src/scss/primary_variables.scss', 'dipl_web_ui_enhanced/static/src/**/*.variables.scss'),
            ('before', 'web/static/src/scss/primary_variables.scss', 'dipl_web_ui_enhanced/static/src/scss/primary_variables.scss'),
        ],
        'web._assets_secondary_variables': [
            ('before', 'web/static/src/scss/secondary_variables.scss', 'dipl_web_ui_enhanced/static/src/scss/secondary_variables.scss'),
        ],
        'web._assets_backend_helpers': [
            ('before', 'web/static/src/scss/bootstrap_overridden.scss', 'dipl_web_ui_enhanced/static/src/scss/bootstrap_overridden.scss'),
        ],
        'web.assets_frontend': [
            'dipl_web_ui_enhanced/static/src/webclient/home_menu/home_menu_background.scss',
            'dipl_web_ui_enhanced/static/src/webclient/navbar/navbar.scss',
        ],
        'web.assets_backend': [
            'dipl_web_ui_enhanced/static/src/webclient/**/*.scss',
            'dipl_web_ui_enhanced/static/src/views/**/*.scss',
            'dipl_web_ui_enhanced/static/src/core/**/*',
            'dipl_web_ui_enhanced/static/src/webclient/**/*.js',
            ('after', 'web/static/src/views/list/list_renderer.xml', 'dipl_web_ui_enhanced/static/src/views/list/list_renderer_desktop.xml'),
            'dipl_web_ui_enhanced/static/src/webclient/**/*.xml',
            'dipl_web_ui_enhanced/static/src/views/**/*.js',
            'dipl_web_ui_enhanced/static/src/views/**/*.xml',
            ('remove', 'dipl_web_ui_enhanced/static/src/views/pivot/**'),
            ('remove', 'dipl_web_ui_enhanced/static/src/**/*.dark.scss'),
        ],
        'web.assets_backend_lazy': [
            'dipl_web_ui_enhanced/static/src/views/pivot/**',
        ],
        'web.assets_backend_lazy_dark': [
            ('include', 'web.dark_mode_variables'),
            ('before', 'dipl_web_ui_enhanced/static/src/scss/bootstrap_overridden.scss', 'dipl_web_ui_enhanced/static/src/scss/bootstrap_overridden.dark.scss'),
            ('after', 'web/static/lib/bootstrap/scss/_functions.scss', 'dipl_web_ui_enhanced/static/src/scss/bs_functions_overridden.dark.scss'),
        ],
        'web.assets_web': [
            ('replace', 'web/static/src/main.js', 'dipl_web_ui_enhanced/static/src/main.js'),
        ],
        "web.dark_mode_variables": [
            ('before', 'dipl_web_ui_enhanced/static/src/scss/primary_variables.scss', 'dipl_web_ui_enhanced/static/src/scss/primary_variables.dark.scss'),
            ('before', 'dipl_web_ui_enhanced/static/src/**/*.variables.scss', 'dipl_web_ui_enhanced/static/src/**/*.variables.dark.scss'),
            ('before', 'dipl_web_ui_enhanced/static/src/scss/secondary_variables.scss', 'dipl_web_ui_enhanced/static/src/scss/secondary_variables.dark.scss'),
        ],
        "web.assets_web_dark": [
            ('include', 'web.dark_mode_variables'),
            ('before', 'dipl_web_ui_enhanced/static/src/scss/bootstrap_overridden.scss', 'dipl_web_ui_enhanced/static/src/scss/bootstrap_overridden.dark.scss'),
            ('after', 'web/static/lib/bootstrap/scss/_functions.scss', 'dipl_web_ui_enhanced/static/src/scss/bs_functions_overridden.dark.scss'),
            'dipl_web_ui_enhanced/static/src/**/*.dark.scss',
        ],
    },
    'author': 'Dipleg',
    'website': 'https://dipleg.com',
    'license': 'LGPL-3',
    'installable': True,
}
