# -*- coding: utf-8 -*-
#############################################################################
#
#  ITL Bangladesh Limited
#
#############################################################################
from odoo import fields, models


class AccountMove(models.Model):
    """ This class extends the functionality of the 'account.move' model to
    include a reference to a help ticket through the 'ticket_id' field."""
    _inherit = 'account.move'

    ticket_id = fields.Many2one('help.ticket', string='Ticket',
                                help='Choose the tickets')
