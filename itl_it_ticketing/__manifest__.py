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

        'data/ir_sequence_data.xml',
        'data/ticket_stage_data.xml',
        'data/helpdesk_types_data.xml',
        'data/product_chain_data.xml',
        'data/ir_cron_data.xml',
        'data/mail_template_data.xml',
        'wizard/ticket_stage_update_wizard_form.xml',
        'wizard/import_help_ticket_wizard_view.xml',

        'views/help_team_views.xml',
        'views/portal_search_templates.xml',
        'views/res_config_settings_views.xml',
        'views/website_form.xml',
        'views/report_templates.xml',
        'views/help_ticket_views.xml',
        'views/portal_views_templates.xml',
        'views/helpdesk_categories_views.xml',
        'views/rating_form_templates.xml',
        'views/merge_tickets_views.xml',
        'views/helpdesk_tag_views.xml',
        'views/helpdesk_types_views.xml',
        'views/ticket_stage_views.xml',
        'views/chain_conf_view.xml',
        'views/helpdesk_replay_template.xml',
        'views/itl_it_ticketing_menus.xml',
        'views/correction_ticket_view.xml',
        'report/help_ticket_templates.xml',
        'scheduler/pending_days_count_view.xml',
    ],
    'assets': {
        'web.assets_backend': [
            'itl_it_ticketing/static/src/xml/help_ticket_templates.xml',
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
