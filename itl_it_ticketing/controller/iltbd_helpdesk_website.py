# -*- coding: utf-8 -*-
#############################################################################
#    ITL BD Ticketing system
#    Md. Aminul Islam
#############################################################################
import datetime as DT
from odoo import http
from odoo.http import request, _logger


class HelpDeskDashboard(http.Controller):
    """Website helpdesk dashboard"""

    @http.route(['/itlbd_ticketing_dashboard'], type='json', auth="public")
    def itlbd_ticketing_dashboard(self):
        """Helpdesk dashboard controller"""
        stage_new = request.env['it.itl.bd.ticket.stage'].search(
            [('name', '=', 'Inbox')], limit=1).id
        stage_draft = request.env['it.itl.bd.ticket.stage'].search(
            [('name', '=', 'Draft')], limit=1).id

        stage_ids = [stage_new, stage_draft]
        new = request.env["it.itl.bd.help.ticket"].search_count(
            [('stage_id', 'in', stage_ids)])
        new_id = request.env["it.itl.bd.help.ticket"].search(
            [('stage_id', 'in', stage_ids)])
        new_id_ls = [data.id for data in new_id]
        # In MIS
        stage_mis = request.env['it.itl.bd.ticket.stage'].search(
            [('name', '=', 'MIS')], limit=1).id
        in_mis = request.env["it.itl.bd.help.ticket"].search_count(
            [('stage_id', '=', stage_mis)])
        in_mis_id = request.env["it.itl.bd.help.ticket"].search(
            [('stage_id', '=', stage_mis)])
        in_mis_ls = [data.id for data in in_mis_id]

        # In On Hold
        stage_cs = request.env['it.itl.bd.ticket.stage'].search(
            [('name', '=', 'On Hold')], limit=1).id
        cs = request.env["it.itl.bd.help.ticket"].search_count(
            [('stage_id', '=', stage_cs)])
        cs_id = request.env["it.itl.bd.help.ticket"].search(
            [('stage_id', '=', stage_cs)])
        cs_id_ls = [data.id for data in cs_id]

        # In Progress
        stage_inprogress = request.env['it.itl.bd.ticket.stage'].search(
            [('name', '=', 'In Progress')], limit=1).id
        in_progress = request.env["it.itl.bd.help.ticket"].search_count(
            [('stage_id', '=', stage_inprogress)])
        in_progress_id = request.env["it.itl.bd.help.ticket"].search(
            [('stage_id', '=', stage_inprogress)])
        in_progress_ls = [data.id for data in in_progress_id]
        # Cancelled
        stage_canceled = request.env['it.itl.bd.ticket.stage'].search(
            [('name', '=', 'Canceled')], limit=1).id
        canceled = request.env["it.itl.bd.help.ticket"].search_count(
            [('stage_id', '=', stage_canceled)])
        canceled_id = request.env["it.itl.bd.help.ticket"].search(
            [('stage_id', '=', stage_canceled)])
        canceled_id_ls = [data.id for data in canceled_id]
        # Verification
        stage_verification = request.env['it.itl.bd.ticket.stage'].search(
            [('name', '=', 'Verification')], limit=1).id
        verification = request.env["it.itl.bd.help.ticket"].search_count(
            [('stage_id', '=', stage_verification)])
        verification_id = request.env["it.itl.bd.help.ticket"].search(
            [('stage_id', '=', stage_verification)])  # Corrected
        verification_id_ls = [data.id for data in verification_id]
        # Done
        stage_done = request.env['it.itl.bd.ticket.stage'].search(
            [('name', '=', 'Done')], limit=1).id
        done = request.env["it.itl.bd.help.ticket"].search_count(
            [('stage_id', '=', stage_done)])
        done_id = request.env["it.itl.bd.help.ticket"].search(
            [('stage_id', '=', stage_done)])
        done_id_ls = [data.id for data in done_id]
        # Correction
        stage_correction = request.env['it.itl.bd.ticket.stage'].search(
            [('name', '=', 'Correction')], limit=1).id
        correction = request.env["it.itl.bd.help.ticket"].search_count(
            [('stage_id', '=', stage_correction)])
        correction_id = request.env["it.itl.bd.help.ticket"].search(
            [('stage_id', '=', stage_correction)])
        correction_id_ls = [data.id for data in correction_id]

        # Close
        stage_closed = request.env['it.itl.bd.ticket.stage'].search(
            [('name', '=', 'Closed')], limit=1).id
        closed = request.env["it.itl.bd.help.ticket"].search_count(
            [('stage_id', '=', stage_closed)])
        closed_id = request.env["it.itl.bd.help.ticket"].search(
            [('stage_id', '=', stage_closed)])
        closed_id_ls = [data.id for data in closed_id]
        dashboard_values = {
            'new': new,
            'in_mis': in_mis,
            'cs': cs,
            'in_progress': in_progress,
            'verification': verification,
            'canceled': canceled,
            'done': done,
            'correction': correction,
            'closed': closed,
            'new_id': new_id_ls,
            'in_mis_id': in_mis_ls,
            'cs_id': cs_id_ls,
            'in_progress_id': in_progress_ls,
            'verification_id': verification_id_ls,
            'canceled_id': canceled_id_ls,
            'done_id': done_id_ls,
            'correction_id': correction_id_ls,
            'closed_id': closed_id_ls,
        }
        return dashboard_values




    @http.route(['/itlbd_ticketing_dashboard_week'], type='json', auth="public")
    def itlbd_ticketing_dashboard_week(self):
        """Week based sorting controller"""
        today = DT.date.today()
        stage_new = request.env['it.itl.bd.ticket.stage'].search(
            [('name', '=', 'Inbox')], limit=1).id
        stage_draft = request.env['it.itl.bd.ticket.stage'].search(
            [('name', '=', 'Draft')], limit=1).id

        stage_done = request.env['it.itl.bd.ticket.stage'].search(
            [('name', '=', 'Done')], limit=1).id
        stage_closed = request.env['it.itl.bd.ticket.stage'].search(
            [('name', '=', 'Closed')], limit=1).id
        stage_ids = [stage_new, stage_draft]
        week_ago = str(today - DT.timedelta(days=7)) + ' '
        new = request.env["it.itl.bd.help.ticket"].search_count(
            [('stage_id', 'in', stage_ids), ('create_date', '>', week_ago)])
        new_id = request.env["it.itl.bd.help.ticket"].search(
            [('stage_id', 'in', stage_ids), ('create_date', '>', week_ago)])
        new_id_ls = [data.id for data in new_id]
        # mis
        stage_mis = request.env['it.itl.bd.ticket.stage'].search(
            [('name', '=', 'MIS')], limit=1).id
        in_mis = request.env["it.itl.bd.help.ticket"].search_count(
            [('stage_id', '=', stage_mis)])
        in_mis_id = request.env["it.itl.bd.help.ticket"].search(
            [('stage_id', '=', stage_mis)])
        in_mis_ls = [data.id for data in in_mis_id]

        # In On Hold
        stage_cs = request.env['it.itl.bd.ticket.stage'].search(
            [('name', '=', 'On Hold')], limit=1).id
        cs = request.env["it.itl.bd.help.ticket"].search_count(
            [('stage_id', '=', stage_cs)])
        cs_id = request.env["it.itl.bd.help.ticket"].search(
            [('stage_id', '=', stage_cs)])
        cs_id_ls = [data.id for data in cs_id]

        # In progress
        stage_inprogress = request.env['it.itl.bd.ticket.stage'].search(
            [('name', '=', 'In Progress')], limit=1).id
        in_progress = request.env["it.itl.bd.help.ticket"].search_count(
            [('stage_id', '=', stage_inprogress),
             ('create_date', '>', week_ago)])
        in_progress_id = request.env["it.itl.bd.help.ticket"].search(
            [('stage_id', '=', stage_inprogress),
             ('create_date', '>', week_ago)])
        in_progress_ls = [data.id for data in in_progress_id]
        # Cancelled
        stage_canceled = request.env['it.itl.bd.ticket.stage'].search(
            [('name', '=', 'Canceled')], limit=1).id
        canceled = request.env["it.itl.bd.help.ticket"].search_count(
            [('stage_id', '=', stage_canceled),
             ('create_date', '>', week_ago)])
        canceled_id = request.env["it.itl.bd.help.ticket"].search(
            [('stage_id', '=', stage_canceled),
             ('create_date', '>', week_ago)])
        canceled_id_ls = [data.id for data in canceled_id]
        # Verification
        stage_verification = request.env['it.itl.bd.ticket.stage'].search(
            [('name', '=', 'Verification')], limit=1).id
        verification = request.env["it.itl.bd.help.ticket"].search_count(
            [('stage_id', '=', stage_verification),
             ('create_date', '>', week_ago)])
        verification_id = request.env["it.itl.bd.help.ticket"].search(
            [('stage_id', '=', stage_verification),
             ('create_date', '>', week_ago)])
        verification_id_ls = [data.id for data in verification_id]
        # Done
        done = request.env["it.itl.bd.help.ticket"].search_count(
            [('stage_id', '=', stage_done), ('create_date', '>', week_ago)])
        done_id = request.env["it.itl.bd.help.ticket"].search(
            [('stage_id', '=', stage_done), ('create_date', '>', week_ago)])
        done_id_ls = [data.id for data in done_id]
        # Correction
        stage_correction = request.env['it.itl.bd.ticket.stage'].search(
            [('name', '=', 'Correction')], limit=1).id
        correction = request.env["it.itl.bd.help.ticket"].search_count(
            [('stage_id', '=', stage_correction), ('create_date', '>', week_ago)])
        correction_id = request.env["it.itl.bd.help.ticket"].search(
            [('stage_id', '=', stage_correction), ('create_date', '>', week_ago)])
        correction_id_ls = [data.id for data in correction_id]
        closed = request.env["it.itl.bd.help.ticket"].search_count(
            [('stage_id', '=', stage_closed), ('create_date', '>', week_ago)])
        closed_id = request.env["it.itl.bd.help.ticket"].search(
            [('stage_id', '=', stage_closed), ('create_date', '>', week_ago)])
        closed_id_ls = [data.id for data in closed_id]
        dashboard_values = {
            'new': new,
            'in_mis': in_mis,
            'cs': cs,
            'in_progress': in_progress,
            'verification': verification,
            'canceled': canceled,
            'done': done,
            'correction': correction,
            'closed': closed,
            'new_id': new_id_ls,
            'in_mis_id': in_mis_ls,
            'cs_id': cs_id_ls,
            'in_progress_id': in_progress_ls,
            'verification_id': verification_id_ls,
            'canceled_id': canceled_id_ls,
            'done_id': done_id_ls,
            'correction_id': correction_id_ls,
            'closed_id': closed_id_ls,
        }
        return dashboard_values

    @http.route(['/itlbd_ticketing_dashboard_month'], type='json', auth="public")
    def itlbd_ticketing_dashboard_month(self):
        """Month based sorting controller"""
        today = DT.date.today()
        stage_new = request.env['it.itl.bd.ticket.stage'].search(
            [('name', '=', 'Inbox')], limit=1).id
        stage_draft = request.env['it.itl.bd.ticket.stage'].search(
            [('name', '=', 'Draft')], limit=1).id
        stage_ids = [stage_new, stage_draft]
        week_ago = str(today - DT.timedelta(days=30)) + ' '
        new = request.env["it.itl.bd.help.ticket"].search_count(
            [('stage_id', 'in', stage_ids), ('create_date', '>', week_ago)])
        new_id = request.env["it.itl.bd.help.ticket"].search(
            [('stage_id', 'in', stage_ids), ('create_date', '>', week_ago)])
        new_id_ls = [data.id for data in new_id]
        # mis
        stage_mis = request.env['it.itl.bd.ticket.stage'].search(
            [('name', '=', 'MIS')], limit=1).id
        in_mis = request.env["it.itl.bd.help.ticket"].search_count(
            [('stage_id', '=', stage_mis)])
        in_mis_id = request.env["it.itl.bd.help.ticket"].search(
            [('stage_id', '=', stage_mis)])
        in_mis_ls = [data.id for data in in_mis_id]
        # In On Hold
        stage_cs = request.env['it.itl.bd.ticket.stage'].search(
            [('name', '=', 'On Hold')], limit=1).id
        cs = request.env["it.itl.bd.help.ticket"].search_count(
            [('stage_id', '=', stage_cs)])
        cs_id = request.env["it.itl.bd.help.ticket"].search(
            [('stage_id', '=', stage_cs)])
        cs_id_ls = [data.id for data in cs_id]

        # In progress
        stage_inprogress = request.env['it.itl.bd.ticket.stage'].search(
            [('name', '=', 'In Progress')], limit=1).id
        in_progress = request.env["it.itl.bd.help.ticket"].search_count(
            [('stage_id', '=', stage_inprogress),
             ('create_date', '>', week_ago)])
        in_progress_id = request.env["it.itl.bd.help.ticket"].search(
            [('stage_id', '=', stage_inprogress),
             ('create_date', '>', week_ago)])
        in_progress_ls = [data.id for data in in_progress_id]

        # Cancelled
        stage_canceled = request.env['it.itl.bd.ticket.stage'].search(
            [('name', '=', 'Canceled')], limit=1).id
        canceled = request.env["it.itl.bd.help.ticket"].search_count(
            [('stage_id', '=', stage_canceled),
             ('create_date', '>', week_ago)])
        canceled_id = request.env["it.itl.bd.help.ticket"].search(
            [('stage_id', '=', stage_canceled),
             ('create_date', '>', week_ago)])
        canceled_id_ls = [data.id for data in canceled_id]
        # Verification
        stage_verification = request.env['it.itl.bd.ticket.stage'].search(
            [('name', '=', 'Verification')], limit=1).id
        verification = request.env["it.itl.bd.help.ticket"].search_count(
            [('stage_id', '=', stage_verification),
             ('create_date', '>', week_ago)])
        verification_id = request.env["it.itl.bd.help.ticket"].search(
            [('stage_id', '=', stage_verification),
             ('create_date', '>', week_ago)])
        verification_id_ls = [data.id for data in verification_id]
        # Done
        stage_done = request.env['it.itl.bd.ticket.stage'].search(
            [('name', '=', 'Done')], limit=1).id
        done = request.env["it.itl.bd.help.ticket"].search_count(
            [('stage_id', '=', stage_done), ('create_date', '>', week_ago)])
        done_id = request.env["it.itl.bd.help.ticket"].search(
            [('stage_id', '=', stage_done), ('create_date', '>', week_ago)])
        done_id_ls = [data.id for data in done_id]
        # Correction
        stage_correction = request.env['it.itl.bd.ticket.stage'].search(
            [('name', '=', 'Correction')], limit=1).id
        correction = request.env["it.itl.bd.help.ticket"].search_count(
            [('stage_id', '=', stage_correction), ('create_date', '>', week_ago)])
        correction_id = request.env["it.itl.bd.help.ticket"].search(
            [('stage_id', '=', stage_correction), ('create_date', '>', week_ago)])
        correction_id_ls = [data.id for data in correction_id]

        # Closed
        stage_closed = request.env['it.itl.bd.ticket.stage'].search(
            [('name', '=', 'Closed')], limit=1).id
        closed = request.env["it.itl.bd.help.ticket"].search_count(
            [('stage_id', '=', stage_closed), ('create_date', '>', week_ago)])
        closed_id = request.env["it.itl.bd.help.ticket"].search(
            [('stage_id', '=', stage_closed), ('create_date', '>', week_ago)])
        closed_id_ls = [data.id for data in closed_id]
        dashboard_values = {
            'new': new,
            'in_mis': in_mis,
            'cs': cs,
            'in_progress': in_progress,
            'verification': verification,
            'canceled': canceled,
            'done': done,
            'correction': correction,
            'closed': closed,
            'new_id': new_id_ls,
            'in_mis_id': in_mis_ls,
            'cs_id': cs_id_ls,
            'in_progress_id': in_progress_ls,
            'verification_id': verification_id_ls,
            'canceled_id': canceled_id_ls,
            'done_id': done_id_ls,
            'correction_id': correction_id_ls,
            'closed_id': closed_id_ls,
        }
        return dashboard_values

    @http.route(['/itlbd_ticketing_dashboard_year'], type='json', auth="public")
    def itlbd_ticketing_dashboard_year(self):
        """Year based sorting"""
        today = DT.date.today()
        stage_new = request.env['it.itl.bd.ticket.stage'].search(
            [('name', '=', 'Inbox')], limit=1).id
        stage_draft = request.env['it.itl.bd.ticket.stage'].search(
            [('name', '=', 'Draft')], limit=1).id

        stage_ids = [stage_new, stage_draft]
        week_ago = str(today - DT.timedelta(days=360)) + ' '
        new = request.env["it.itl.bd.help.ticket"].search_count(
            [('stage_id', 'in', stage_ids), ('create_date', '>', week_ago)])
        new_id = request.env["it.itl.bd.help.ticket"].search(
            [('stage_id', 'in', stage_ids), ('create_date', '>', week_ago)])
        new_id_ls = [data.id for data in new_id]
        # In MIS
        stage_mis = request.env['it.itl.bd.ticket.stage'].search(
            [('name', '=', 'MIS')], limit=1).id
        in_mis = request.env["it.itl.bd.help.ticket"].search_count(
            [('stage_id', '=', stage_mis)])
        in_mis_id = request.env["it.itl.bd.help.ticket"].search(
            [('stage_id', '=', stage_mis)])
        in_mis_ls = [data.id for data in in_mis_id]
        # In On Hold
        stage_cs = request.env['it.itl.bd.ticket.stage'].search(
            [('name', '=', 'On Hold')], limit=1).id
        cs = request.env["it.itl.bd.help.ticket"].search_count(
            [('stage_id', '=', stage_cs)])
        cs_id = request.env["it.itl.bd.help.ticket"].search(
            [('stage_id', '=', stage_cs)])
        cs_id_ls = [data.id for data in cs_id]

        # In progress
        stage_inprogress = request.env['it.itl.bd.ticket.stage'].search(
            [('name', '=', 'In Progress')], limit=1).id
        in_progress = request.env["it.itl.bd.help.ticket"].search_count(
            [('stage_id', '=', stage_inprogress),
             ('create_date', '>', week_ago)])
        in_progress_id = request.env["it.itl.bd.help.ticket"].search(
            [('stage_id', '=', stage_inprogress),
             ('create_date', '>', week_ago)])
        in_progress_ls = [data.id for data in in_progress_id]
        # Cancelled
        stage_canceled = request.env['it.itl.bd.ticket.stage'].search(
            [('name', '=', 'Canceled')], limit=1).id
        canceled = request.env["it.itl.bd.help.ticket"].search_count(
            [('stage_id', '=', stage_canceled),
             ('create_date', '>', week_ago)])
        canceled_id = request.env["it.itl.bd.help.ticket"].search(
            [('stage_id', '=', stage_canceled),
             ('create_date', '>', week_ago)])
        canceled_id_ls = [data.id for data in canceled_id]
        # Verification
        stage_verification = request.env['it.itl.bd.ticket.stage'].search(
            [('name', '=', 'Verification')], limit=1).id
        verification = request.env["it.itl.bd.help.ticket"].search_count(
            [('stage_id', '=', stage_verification),
             ('create_date', '>', week_ago)])
        verification_id = request.env["it.itl.bd.help.ticket"].search(
            [('stage_id', '=', stage_verification),
             ('create_date', '>', week_ago)])
        verification_id_ls = [data.id for data in verification_id]
        # Done
        stage_done = request.env['it.itl.bd.ticket.stage'].search(
            [('name', '=', 'Done')], limit=1).id
        done = request.env["it.itl.bd.help.ticket"].search_count(
            [('stage_id', '=', stage_done), ('create_date', '>', week_ago)])
        done_id = request.env["it.itl.bd.help.ticket"].search(
            [('stage_id', '=', stage_done), ('create_date', '>', week_ago)])
        done_id_ls = [data.id for data in done_id]
        # Correction
        stage_correction = request.env['it.itl.bd.ticket.stage'].search(
            [('name', '=', 'Correction')], limit=1).id
        correction = request.env["it.itl.bd.help.ticket"].search_count(
            [('stage_id', '=', stage_correction), ('create_date', '>', week_ago)])
        correction_id = request.env["it.itl.bd.help.ticket"].search(
            [('stage_id', '=', stage_correction), ('create_date', '>', week_ago)])
        correction_id_ls = [data.id for data in correction_id]
        # Closed
        stage_closed = request.env['it.itl.bd.ticket.stage'].search(
            [('name', '=', 'Closed')], limit=1).id
        closed = request.env["it.itl.bd.help.ticket"].search_count(
            [('stage_id', '=', stage_closed), ('create_date', '>', week_ago)])
        closed_id = request.env["it.itl.bd.help.ticket"].search(
            [('stage_id', '=', stage_closed), ('create_date', '>', week_ago)])
        closed_id_ls = [data.id for data in closed_id]
        dashboard_values = {
            'new': new,
            'in_mis': in_mis,
            'cs': cs,
            'in_progress': in_progress,
            'verification': verification,
            'canceled': canceled,
            'done': done,
            'correction': correction,
            'closed': closed,
            'new_id': new_id_ls,
            'in_mis_id': in_mis_ls,
            'cs_id': cs_id_ls,
            'in_progress_id': in_progress_ls,
            'verification_id': verification_id_ls,
            'canceled_id': canceled_id_ls,
            'done_id': done_id_ls,
            'correction_id': correction_id_ls,
            'closed_id': closed_id_ls,
        }
        return dashboard_values
