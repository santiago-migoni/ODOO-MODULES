{
    'name': 'web_enhanced',
    'version': '1.0',
    'category': 'Extra Tools',
    'summary': 'Módulo personalizado para mejorar la interfaz web de Odoo Community',
    'author': 'Dipleg',
    'depends': ['web', 'base_setup'],
    'data': [
        'security/ir.model.access.csv',
        'views/views.xml',
        'views/webclient_templates.xml',
    ],
    'assets': {
        'web._assets_primary_variables': [
            ('after', 'web/static/src/scss/primary_variables.scss', 'dipl_web_enhanced/static/src/**/*.variables.scss'),
            ('before', 'web/static/src/scss/primary_variables.scss', 'dipl_web_enhanced/static/src/scss/primary_variables.scss'),
        ],
        'web._assets_secondary_variables': [
            ('before', 'web/static/src/scss/secondary_variables.scss', 'dipl_web_enhanced/static/src/scss/secondary_variables.scss'),
        ],
        'web._assets_backend_helpers': [
            ('before', 'web/static/src/scss/bootstrap_overridden.scss', 'dipl_web_enhanced/static/src/scss/bootstrap_overridden.scss'),
        ],
        'web.assets_frontend': [
            'dipl_web_enhanced/static/src/webclient/home_menu/home_menu_background.scss',
            'dipl_web_enhanced/static/src/webclient/navbar/navbar.scss',
        ],
        'web.assets_backend': [
            'dipl_web_enhanced/static/src/webclient/**/*.scss',
            'dipl_web_enhanced/static/src/views/**/*.scss',
            'dipl_web_enhanced/static/src/core/**/*',
            'dipl_web_enhanced/static/src/webclient/**/*.js',
            ('after', 'web/static/src/views/list/list_renderer.xml', 'dipl_web_enhanced/static/src/views/list/list_renderer_desktop.xml'),
            'dipl_web_enhanced/static/src/webclient/**/*.xml',
            'dipl_web_enhanced/static/src/views/**/*.js',
            'dipl_web_enhanced/static/src/views/**/*.xml',
            ('remove', 'dipl_web_enhanced/static/src/views/pivot/**'),
        ],
        'web.assets_backend_lazy': [
            'dipl_web_enhanced/static/src/views/pivot/**',
        ],
        'web.assets_backend_lazy_dark': [
            ('include', 'web.dark_mode_variables'),
            ('before', 'dipl_web_enhanced/static/src/scss/bootstrap_overridden.scss', 'dipl_web_enhanced/static/src/scss/bootstrap_overridden.dark.scss'),
            ('after', 'web/static/lib/bootstrap/scss/_functions.scss', 'dipl_web_enhanced/static/src/scss/bs_functions_overridden.dark.scss'),
        ],
        'web.assets_web': [
            'dipl_web_enhanced/static/src/main.js',
        ],
        'web.dark_mode_variables': [
            ('before', 'dipl_web_enhanced/static/src/scss/primary_variables.scss', 'dipl_web_enhanced/static/src/scss/primary_variables.dark.scss'),
            ('before', 'dipl_web_enhanced/static/src/**/*.variables.scss', 'dipl_web_enhanced/static/src/**/*.variables.dark.scss'),
            ('before', 'dipl_web_enhanced/static/src/scss/secondary_variables.scss', 'dipl_web_enhanced/static/src/scss/secondary_variables.dark.scss'),
        ],
        'web.assets_web_dark': [
            ('include', 'web.dark_mode_variables'),
            ('before', 'dipl_web_enhanced/static/src/scss/bootstrap_overridden.scss', 'dipl_web_enhanced/static/src/scss/bootstrap_overridden.dark.scss'),
            ('after', 'web/static/lib/bootstrap/scss/_functions.scss', 'dipl_web_enhanced/static/src/scss/bs_functions_overridden.dark.scss'),
        ],
        'web.assets_tests': [
            'dipl_web_enhanced/static/tests/tours/**/*',
        ],
    },
    'installable': True,
    'license': 'LGPL-3',
}