# -*- coding: utf-8 -*-
#############################################################################
#   ITL BD Limited
#   itl-group.com
#############################################################################
from odoo import http
from odoo.addons.portal.controllers import portal
from odoo.http import request


class TicketPortal(portal.CustomerPortal):
    """ Controller for handling customer portal related actions related to
    helpdesk tickets.
    """
    def _prepare_home_portal_values(self, counters):
        """Prepares a dictionary of values to be used in the home portal view
        and get their count."""
        values = super()._prepare_home_portal_values(counters)
        if 'ticket_count' in counters:
            ticket_count = request.env['help.ticket'].search_count(
                self._get_tickets_domain()) if request.env[
                'help.ticket'].check_access_rights(
                'read', raise_exception=False) else 0
            values['ticket_count'] = ticket_count
        return values

    def _get_tickets_domain(self):
        """Checking the domain"""
        return [('customer_id', '=', request.env.user.partner_id.id)]

    @http.route(['/my/tickets'], type='http', auth="user", website=True)
    def portal_my_tickets(self):
        """Displays a list of tickets for the current user in the user's
        portal."""
        domain = self._get_tickets_domain()
        tickets = request.env['help.ticket'].search(domain)
        values = {
            'default_url': "/my/tickets",
            'tickets': tickets,
            'page_name': 'ticket',
        }
        return request.render("itl_it_ticketing.portal_my_tickets",
                              values)

    @http.route(['/my/tickets/<int:id>'], type='http', auth="public",
                website=True)
    def portal_tickets_details(self, id):
        """Displays a list of tickets for the current user in the user's
        portal."""
        details = request.env['help.ticket'].sudo().search([('id', '=', id)])
        data = {
            'page_name': 'ticket',
            'ticket': True,
            'details': details,
        }
        return request.render("itl_it_ticketing.portal_ticket_details",data)

    @http.route('/my/tickets/download/<id>', auth='public',
                type='http',
                website=True)
    def ticket_download_portal(self, id):
        """Download the ticket information in a pdf formate of the current
         event ticket."""
        data = {
            'help': request.env['help.ticket'].sudo().browse(int(id))}
        report = request.env.ref(
            'itl_it_ticketing.action_report_helpdesk_ticket')
        pdf, _ = request.env.ref(
            'itl_it_ticketing.action_report_helpdesk_ticket').sudo()._render_qweb_pdf(
            report, data=data)
        pdf_http_headers = [('Content-Type', 'application/pdf'),
                            ('Content-Length', len(pdf)),
                            ('Content-Disposition',
                             'attachment; filename="Helpdesk Ticket.pdf"')]
        return request.make_response(pdf, headers=pdf_http_headers)


class WebsiteDesk(http.Controller):
    """Control for handling the helpdesk tickets form and its submission."""
    @http.route(['/helpdesk_ticket'], type='http', auth="public",
                website=True, sitemap=True)
    def helpdesk_ticket(self):
        """Render the helpdesk ticket form."""
        types = request.env['helpdesk.types'].sudo().search([])
        categories = request.env['helpdesk.categories'].sudo().search([])
        product = request.env['product.template'].sudo().search([])
        values = {}
        values.update({
            'types': types,
            'categories': categories,
            'product_website': product
        })
        return request.render('itl_it_ticketing.ticket_form', values)

    @http.route(['/rating/<int:ticket_id>'], type='http', auth="public",
                website=True,
                sitemap=True)
    def rating(self, ticket_id):
        """Render the helpdesk ticket rating form."""
        ticket = request.env['help.ticket'].browse(ticket_id)
        data = {
            'ticket': ticket.id,
        }
        return request.render('itl_it_ticketing.rating_form', data)

    @http.route(['/rating/<int:ticket_id>/submit'], type='http',
                auth="user",
                website=True, csrf=False,
                sitemap=True)
    def rating_backend(self, ticket_id, **post):
        """Render the thanks page after rating the helpdesk ticket."""
        ticket = request.env['help.ticket'].browse(ticket_id)
        ticket.write({
            'customer_rating': post['rating'],
            'review': post['message'],
        })
        return request.render('itl_it_ticketing.rating_thanks')
