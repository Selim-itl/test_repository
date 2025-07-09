# -*- coding: utf-8 -*-
#############################################################################
# ITL Bangladesh Limited
#
#############################################################################
from odoo import fields, models


class SupportTickets(models.Model):
    """Creating onetoMany model to handle the merging ticket"""
    _name = 'support.tickets'
    _description = 'Support Tickets'

    subject = fields.Char(string='Subject', help='Subject of the merged '
                                                 'tickets')
    display_name = fields.Char(string='Display Name',
                               help='Display name of the merged tickets')
    description = fields.Char(string='Description',
                              help='Description of the tickets')
    support_ticket_id = fields.Many2one('merge.tickets',
                                        string='Support Tickets',
                                        help='Support tickets')
    merged_ticket = fields.Integer(string='Merged Ticket ID',
                                   help='Storing merged ticket id')
