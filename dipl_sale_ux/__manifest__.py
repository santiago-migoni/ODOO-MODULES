# -*- coding: utf-8 -*-
{
    'name': 'DIPL - Filtro de Cotizaciones Activas',
    'version': '19.0.1.0.0',
    'category': 'Sales',
    'summary': 'Filtro predeterminado para mostrar cotizaciones vigentes',
    'description': """
        Mejora de UX para el módulo de ventas:
        
        Características:
        - Filtro predeterminado "Cotizaciones" en la vista de cotizaciones
        - Muestra solo cotizaciones en estado borrador/enviadas que no han vencido
        - Los usuarios pueden desactivar el filtro si necesitan ver todas las cotizaciones
        - Mejora la productividad al enfocarse en cotizaciones relevantes
        
        Criterios del filtro:
        - Estado: Borrador (draft) o Enviada (sent)
        - Fecha de validez: Mayor o igual a hoy, o sin fecha definida
    """,
    'author': 'DIPLEG',
    'website': '',
    'depends': ['sale'],
    'data': [
        'views/sale_order_views.xml',
    ],
    'installable': True,
    'application': False,
    'auto_install': False,
    'license': 'LGPL-3',
}
