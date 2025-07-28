# -*- coding: utf-8 -*-
#############################################################################
# ----------------------------------------------------------------------------
#    ITL Bangladesh Limited
#
#############################################################################
{
    'name': "IT Ticketing",
    'version': '16.0.3.0.0',
    'category': 'Website',
    'summary': """IT ticketing module for IT support team""",
    'description': 'Can create ticket from eamil and portal. Can manage it from portal.',
    'author': "ITL",
    'company': 'ITL',
    'depends': ['base', 'hr','website', 'project', 'sale_project',
                'hr_timesheet', 'mail', 'contacts'],
    'data': [
        'security/itl_it_ticketing_security.xml',
        'security/ir.model.access.csv',

        'data/itlbd_ir_sequence_data.xml',
        'data/itlbd_ticket_stage_data.xml',
        'data/itlbd_helpdesk_types_data.xml',
        'data/itlbd_product_chain_data.xml',
        'data/itlbd_ir_cron_data.xml',
        'data/itlbd_mail_template_data.xml',
        'data/status_change_mail_template.xml',
        'wizard/itlbd_ticket_stage_update_wizard_form.xml',
        'wizard/itlbd_import_help_ticket_wizard_view.xml',

        'views/itlbd_help_team_views.xml',
        'views/itlbd_portal_search_templates.xml',
        # 'views/itlbd_res_config_settings_views.xml',
        'views/itlbd_website_form.xml',
        'views/itlbd_report_templates.xml',
        'views/itlbd_help_ticket_views.xml',
        'views/itlbd_portal_views_templates.xml',
        'views/itlbd_helpdesk_categories_views.xml',
        'views/itlbd_rating_form_templates.xml',
        'views/itlbd_merge_tickets_views.xml',
        'views/itlbd_helpdesk_tag_views.xml',
        'views/itlbd_helpdesk_types_views.xml',
        'views/itlbd_ticket_stage_views.xml',
        'views/itlbd_chain_conf_view.xml',
        'views/itlbd_helpdesk_replay_template.xml',
        'views/itlbd_itl_it_ticketing_menus.xml',
        'views/itlbd_correction_ticket_view.xml',
        'report/itlbd_help_ticket_templates.xml',
        'scheduler/itlbd_pending_days_count_view.xml',
    ],
    'assets': {
        'web.assets_backend': [
            'itl_it_ticketing/static/src/xml/itlbd_help_ticket_templates.xml',
            'itl_it_ticketing/static/src/js/helpdesk_dashboard_action.js',
        ],
        'web.assets_frontend': [
            'itl_it_ticketing/static/src/js/ticket_details.js',
            '/itl_it_ticketing/static/src/js/portal_groupby_and_search.js',
            '/itl_it_ticketing/static/src/js/multiple_product_choose.js',
            '/itl_it_ticketing/static/src/cdn/jquery.sumoselect.min.js',
            '/itl_it_ticketing/static/src/cdn/sumoselect.min.css',
        ]
    },
    'images': ['static/description/banner.png'],
    'license': 'LGPL-3',
    'installable': True,
    'auto_install': False,
    'application': False,
}
