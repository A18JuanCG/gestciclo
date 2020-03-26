# -*- coding: utf-8 -*-
{
    'name': 'Gestión de ciclos de FP',
   	'summary': """Módulo para la gestión de ciclos de Formación Profesional""",
    'description': """
		Este módulo ofrece una gestión muy básica de un ciclo de FP.
		Es posible insertar alumnos, profesores, asignaturas, etc.
		""",
    'author': "Juan M. Cardeso",
    'website': "http://www.iessanclemente.net",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/12.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base'],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'views/ciclo.xml',
        'views/modulo.xml',
        'views/templates.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}
