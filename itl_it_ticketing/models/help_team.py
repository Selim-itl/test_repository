# -*- coding: utf-8 -*-
#############################################################################
#    ITL Bangladesh Limited
#   Md. Aminul Islam
#############################################################################
from odoo import api, fields, models


class HelpTeam(models.Model):
    """ This class represents a Helpdesk Team in the system, providing
     information about the team members, leader, and related project."""
    _name = 'it.itl.bd.help.team'
    _description = 'Helpdesk Team'

    name = fields.Char(string='Name', help='Name of the Helpdesk Team. It '
                                           'identify the helpdesk team')
    team_lead_id = fields.Many2one(
        'res.users',
        string='Team Leader',
        help='Name of the Helpdesk Team Leader.',
        domain=lambda self: [('groups_id', 'in', self.env.ref(
            'itl_it_ticketing.helpdesk_team_leader').id)])
    member_ids = fields.Many2many(
        'res.users',
        string='Members',
        help='Users who belong to that Helpdesk Team',
        domain=lambda self: [('groups_id', 'in', self.env.ref(
            'itl_it_ticketing.helpdesk_user').id)])
    email = fields.Char(string='Email', help='Email')
    project_id = fields.Many2one('project.project',
                                 string='Project',
                                 help='The Project they are currently in')
    create_task = fields.Boolean(string="Create Task",
                                 help="Enable for allowing team to "
                                      "create tasks from tickets")
    state = fields.Selection([
        ('created', 'Created'),
        ('cancelled', 'Cancelled')], 'Status', default='created', readonly=True)

    ticket_num = fields.Integer(string="Ticket", compute='count_cs_ticket')
    ticket_info = fields.One2many('it.itl.bd.help.ticket', 'team_id', 'Tickets')

    @api.depends('ticket_info')  # Count and Show Ticket from smart button
    def count_cs_ticket(self):
        self.ticket_num = len(self.ticket_info)
        return {
            'name': 'Ticket Management',
            'res_model': 'it.itl.bd.help.ticket',
            'view_mode': 'tree,form',
            'domain': [('team_id', '=', self.name)],
            'type': 'ir.actions.act_window',
            'context': {'default_team_id': self.name}
        }

    @api.onchange('team_lead_id')
    def members_choose(self):
        """ This method is triggered when the Team Leader is changed. It
        updates the available team members based on the selected leader and
        filters out the leader from the list of potential members."""
        fetch_members = self.env['res.users'].search([])
        filtered_members = fetch_members.filtered(
            lambda x: x.id != self.team_lead_id.id)
        return {'domain': {'member_ids': [
            ('id', '=', filtered_members.ids),
            ('groups_id', 'in', self.env.ref('base.group_user').id),
            ('groups_id', 'not in', self.env.ref(
                'itl_it_ticketing.helpdesk_team_leader').id)]}}


    def team_base_ticket(self):
        pass
    def btn_team_cancel(self):
        pass