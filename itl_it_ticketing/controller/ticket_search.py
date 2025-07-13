# -*- coding: utf-8 -*-
#############################################################################
#
#    ITL Bangladesh Pvt. Ltd.
#
#############################################################################
from odoo import http
from odoo.http import request


class TicketSearch(http.Controller):
    """Control for handle the  customer portal search
    filtering by the tickets."""
    @http.route(['/ticketsearch'], type='json', auth="public", website=True)
    def ticket_search(self, **kwargs):
        """ Display the list of tickets satisfying the searching condition.
        Searching the ticket  based on name or subject"""
        search_value = kwargs.get("search_value")
        tickets = request.env["it.itl.bd.help.ticket"].search(
            ['|', ('name', 'ilike', search_value),
             ('subject', 'ilike', search_value)])
        values = {
            'tickets': tickets,
        }
        response = http.Response(template='itl_it_ticketing.ticket_table',
                                 qcontext=values)
        return response.render()
