# -*- coding: utf-8 -*-
{
    'name': "class_attendance",

    'summary': "Short (1 phrase/line) summary of the module's purpose",

    'description': """
Long description of module's purpose
    """,

    'author': "My Company",
    'website': "https://www.yourcompany.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/15.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base','hr','mail',],

    # always loaded
    'data': [
        'security/ir.model.access.csv',

        # data files
        'data/roll_sequence.xml',
        'data/class_attendance_cron.xml',

        # views files
        'views/menu.xml',
        'views/attendance_class.xml',
        'views/section_views.xml',
        'views/subject_views.xml',
        'views/class_class_views.xml',
        'views/student_views.xml',
        'views/classroom_views.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}

