# -*- coding: utf-8 -*-
#############################################################################
# ITL Bangladesh Limited
#
#############################################################################
from odoo import api, fields, models


class ResConfigSettings(models.TransientModel):
    """This class extends the functionality of the 'res.config.settings' model
     to provide configuration options for various settings related to the
     helpdesk module.
   """
    _inherit = 'res.config.settings'

    show_create_task = fields.Boolean(
        string="Create Tasks",
        config_parameter='itl_it_ticketing.show_create_task',
        help='When enabling this field yu can create a task under the ticket')
    show_category = fields.Boolean(
        string="Category",
        config_parameter='itl_it_ticketing.show_category',
        help='When enabling this its show the category of ticket',
        implied_group='itl_it_ticketing.group_show_category_it_itl_bd')
    product_website = fields.Boolean(
        string="Product On Website",
        config_parameter='itl_it_ticketing.product_website',
        help='When enabling this feature you can mention the product on website'
             ' at time of creating the ticketProduct on website')
    auto_close_ticket = fields.Boolean(
        string="Auto Close Ticket",
        config_parameter='itl_it_ticketing.auto_close_ticket',
        help='Automatically Close ticket if the condition is satisfied')
    no_of_days = fields.Integer(
        string="No Of Days",
        config_parameter='itl_it_ticketing.no_of_days',
        help='After this date the ticket will closing automatically ')
    closed_stage = fields.Many2one(
        'it.itl.bd.ticket.stage', string='Closing stage',
        help='Closing Stage',
        config_parameter='itl_it_ticketing.closed_stage')

    reply_template_id = fields.Many2one(
        'mail.template',
        string='Relaid ID',
        domain="[('model', '=', 'it.itl.bd.help.ticket')]",
        config_parameter='itl_it_ticketing.reply_template_id',
        help='Reply Template')
    helpdesk_menu_show = fields.Boolean(
        string='Helpdesk Menu',
        config_parameter='itl_it_ticketing.helpdesk_menu_show',
        help='When enabling this option to visible Helpdesk menu in website')

    @api.onchange('closed_stage')
    def closed_stage_a(self):
        """This method is triggered when the 'closed_stage' field is changed.
         It updates the 'closing_stage' attribute of the selected stage and
         clears it for other stages.
       """
        stage = self.closed_stage.id
        in_stage = self.env['it.itl.bd.ticket.stage'].search([('id', '=', stage)])
        not_in_stage = self.env['it.itl.bd.ticket.stage'].search([('id', '!=', stage)])
        in_stage.closing_stage = True
        for each in not_in_stage:
            each.closing_stage = False

    @api.constrains('show_category')
    def show_category_subcategory(self):
        """ This constraint method is triggered when the 'show_category' field
        is changed. It updates the users in the 'group_show_category_it_itl_bd' based on
        the 'show_category' value.
       """
        if self.show_category:
            group_cat = self.env.ref(
                'itl_it_ticketing.group_show_category_it_itl_bd')
            group_cat.write({
                'users': [(4, self.env.user.id)]
            })
        else:
            group_cat = self.env.ref(
                'itl_it_ticketing.group_show_category_it_itl_bd')
            group_cat.write({
                'users': [(5, False)]
            })
