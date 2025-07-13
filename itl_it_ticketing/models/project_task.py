# -*- coding: utf-8 -*-
#############################################################################
# ITL Bangladesh Limited
#
#############################################################################
from odoo import fields, models


class ProjectTask(models.Model):
    """
    This class extends the 'project.task' model in Odoo to add a custom field
     called 'ticket_billed' and 'ticket_id'.
     ticket_billed: A boolean field indicating whether the ticket has
     been billed or not.
     ticket_id : A many2One field to link the task
    with a help ticket
    """
    _inherit = 'project.task'

    ticket_billed = fields.Boolean(string='Billed',
                                   help='Whether the Ticket has been Invoiced'
                                        'or Not')
    ticket_id = fields.Many2one('it.itl.bd.help.ticket', string='Ticket',
                                help='The help ticket associated with this '
                                     'recordThis field allows you to link '
                                     'this record to an existing help ticket.')
