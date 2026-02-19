# -*- coding: utf-8 -*-
{
    'name': 'DIPL - Cotización por Peso y Minutos',
    'version': '19.0.2.0.0',
    'category': 'Sales',
    'summary': 'Cálculo de precios basado en peso (kg) y minutos de corte',
    'description': """
        Módulo profesional para calcular precios de corte/plegado basados en:
        - Dimensiones (desarrollo, largo, espesor)
        - Peso del material (kg)
        - Minutos de corte láser (opcional)
        
        Características:
        - Redondeo automático a miles
        - Integración con listas de precios y descuentos
        - Suite completa de tests unitarios
        - Logging para debugging
        - Evaluación segura de expresiones matemáticas
        
        Nota: Para usar calculadora en campos numéricos, 
        escribir con = al inicio (ej: =100+200). 
        Esta es funcionalidad nativa de Odoo 19.
    """,
    'author': 'DIPLEG',
    'website': '',
    'depends': ['sale'],
    # 'external_dependencies': {
    #     'python': ['simpleeval'],
    # },
    'data': [
        'security/ir.model.access.csv',
        'data/material_preset_data.xml',
        'views/material_preset_views.xml',
        'views/res_config_settings_views.xml',
        'views/product_views.xml',
        'views/sale_order_views.xml',
        'report/sale_order_report.xml',
    ],
    'installable': True,
    'application': False,
    'auto_install': False,
    'license': 'LGPL-3',
}
