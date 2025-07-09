# -*- coding: utf-8 -*-
{
    "name": "OM Hospital",
    "version": "1.0",
    "category": "Tests",
    "description": """A module to test the Group functionality.""",
    "depends": ["base"],
    "installable": True,
    "data": [
        # 'security/security.xml',
        'security/ir.model.access.csv',
        'views/root_menu_view.xml',
        'views/doctor_view.xml',
        'views/patient_view.xml',
        'views/appointment_view.xml',
        'views/tags_view.xml',
        'views/room_view.xml',
        'report/report_appointment.xml',
        'report/report_patient.xml',
        'report/report_appointment_action.xml'
    ],
    'license': 'LGPL-3',
    "application": True,
}