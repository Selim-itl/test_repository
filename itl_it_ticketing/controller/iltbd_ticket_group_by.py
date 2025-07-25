# -*- coding: utf-8 -*-
#############################################################################
#
#    ITL Bangladesh Pvt. Ltd.
#
#############################################################################
from odoo import http
from odoo.http import request


class TicketGroupBy(http.Controller):
    """Control for handle the  customer portal groupBy
    filtering by the tickets."""
    @http.route(['/ticketgroupby'], type='json', auth="public", website=True)
    def ticket_group_by(self, **kwargs):
        """Display the list of tickets based on the groupBy filtering"""
        context = []
        group_value = kwargs.get("search_value")
        if group_value == '0':
            context = []
            tickets = request.env["it.itl.bd.help.ticket"].search([])
            context.append(tickets)
        if group_value == '1':
            context = []
            stage_ids = request.env['it.itl.bd.ticket.stage'].search([])
            for stage in stage_ids:
                ticket_ids = request.env['it.itl.bd.help.ticket'].search([
                    ('stage_id', '=', stage.id)
                ])
                if ticket_ids:
                    context.append({
                        'name': stage.name,
                        'data': ticket_ids
                    })
        if group_value == '2':
            context = []
            type_ids = request.env['it.itl.bd.helpdesk.types'].search([])
            for types in type_ids:
                ticket_ids_1 = request.env['it.itl.bd.help.ticket'].search([
                    ('ticket_type', '=', types.id)
                ])
                if ticket_ids_1:
                    context.append({
                        'name': types.name,
                        'data': ticket_ids_1
                    })
        values = {
            'tickets': context,
        }
        response = http.Response(
            template='itl_it_ticketing.ticket_group_by_table_it_itl_bd',
            qcontext=values)
        return response.render()
