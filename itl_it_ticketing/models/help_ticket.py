# -*- coding: utf-8 -*-
#############################################################################
# ITL Bangladesh Pvt. Limited.
#
#############################################################################
import logging
from odoo import api, fields, models, _
from odoo.exceptions import UserError
from odoo.exceptions import ValidationError
from datetime import datetime
_logger = logging.getLogger(__name__)

PRIORITIES = [
    ('0', 'Very Low'),
    ('1', 'Low'),
    ('2', 'Normal'),
    ('3', 'High'),
    ('4', 'Very High'),
]
RATING = [
    ('0', 'Very Low'),
    ('1', 'Low'),
    ('2', 'Normal'),
    ('3', 'High'),
    ('4', 'Very High'),
    ('5', 'Extreme High')
]


class HelpTicket(models.Model):
    """This model represents the Helpdesk Ticket, which allows users to raise
    tickets related to products, services or any other issues. Each ticket has a
    name, customer information, description, team responsible for handling
    requests, associated project, priority level, stage, cost per hour, service
    product, start and end dates, and related tasks and invoices."""

    _name = 'help.ticket'
    _description = 'Help Ticket'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char(string='Ticket No',
                       help='The name of the help ticket. By default, a new '
                            'unique sequence number is assigned to each '
                            'help ticket, unless a name is provided.', readonly=True)
    active = fields.Boolean(default=True, help='Active', string='Active')
    customer_id = fields.Many2one('res.partner',
                                  string='Customer Name',
                                  help='Select the Customer Name')
    subject = fields.Text(string='Subject', required=True,
                          help='Subject of the Ticket')
    description = fields.Text(string='Description',
                              help='Issue Description')
    email = fields.Char(string='Email', help='Email of the User.')
    phone = fields.Char(string='Phone', help='Phone Number of the user')
    team_id = fields.Many2one('help.team', string='Helpdesk Team',
                              help='The helpdesk team responsible for '
                                   'handling requests related to this '
                                   'record')
    product_ids = fields.Many2many('product.template',
                                   string='Product',
                                   help='The product associated with this '
                                        'record.This field allows you to select'
                                        'an existing product from the product '
                                        'catalog.')

    project_id = fields.Many2one('project.project',
                                 string='Project',
                                 readonly=False,
                                 related='team_id.project_id',
                                 store=True,
                                 invisible=True,
                                 help='The project associated with this team.'
                                      'This field is automatically filled '
                                      'based on the project assigned to '
                                      'the team.')
    priority = fields.Selection(PRIORITIES,
                                default='1',
                                help='Set the priority level',
                                string='Priority')

    user_id = fields.Many2one('res.users',
                              default=lambda self: self.env.user,
                              check_company=True,
                              index=True, tracking=True,
                              help='Login User', string="Create By")
    cost = fields.Float(string='Cost per hour',
                        help='The cost per hour for this record. This field '
                             'specifies the hourly cost associated with the'
                             'record, which can be used in various '
                             'calculations or reports.')
    service_product_id = fields.Many2one('product.product',
                                         string='Service Product',
                                         help='The product associated with this'
                                              'service. Only service products '
                                              'are available for selection.',
                                         domain=[
                                             ('detailed_type', '=', 'service')])
    create_date = fields.Datetime(string='Creation Date', help='Created date of'
                                                               'the Ticket')
    start_date = fields.Datetime(string='Start Date', help='Start Date of the' 'Ticket')
    end_date = fields.Datetime(string='End Date', help='End Date of the Ticket')
    required_date = fields.Datetime(string='Required Date', help='Required Date of the Ticket')
    public_ticket = fields.Boolean(string="Public Ticket", help='Public Ticket')
    invoice_ids = fields.Many2many('account.move',
                                   string='Invoices',
                                   help='To Generate Invoice based on hours '
                                        'spent on the ticket'
                                   )
    task_ids = fields.Many2many('project.task',
                                string='Tasks',
                                help='Related Task of the Ticket')
    color = fields.Integer(string="Color", help='Color')
    replied_date = fields.Datetime(string='Replied date',
                                   help='Replied Date of the Ticket')
    last_update_date = fields.Datetime(string='Last Update Date',
                                       help='Last Update Date of Ticket')
    ticket_type = fields.Many2one('helpdesk.types',
                                  string='Ticket Type', help='Ticket Type')
    team_head = fields.Many2one('res.users', string='Team Leader',
                                compute='_compute_team_head',
                                help='Team Leader Name', store=True)
    assigned_user = fields.Many2many(
        'res.users',
        string='Ticket Owner',
        domain=lambda self: [('groups_id', 'in', self.env.ref(
            'itl_it_ticketing.helpdesk_user').id)],
        help='Choose the Assigned User Name')

    category_id = fields.Many2one('helpdesk.categories',
                                  help='Choose the Category', string='Category')
    tags = fields.Many2many('helpdesk.tag', help='Choose the Tags',
                            string='Tag')
    assign_user = fields.Boolean(string='Assigned User', help='Assign User')
    attachment_ids = fields.One2many('ir.attachment',
                                     'res_id',
                                     help='Attachment Line',
                                     string='Attachment')
    merge_ticket_invisible = fields.Boolean(string='Merge Ticket',
                                            help='Merge Ticket Invisible or '
                                                 'Not')
    merge_count = fields.Integer(string='Merge Count', help='Merged Tickets '
                                                           'Count')

    # customize
    chain_ids = fields.Many2many('chain.conf',
                                   string='Select Chain',
                                   help='The Order associated with this '
                                        'record.This field allows you to select'
                                        'an existing chain from the chain '
                                        'catalog.')

    employee_ids = fields.Many2many('hr.employee',
                                 string='CS',
                                 help='CS Owners')

    job_reference = fields.Char(string='Job Reference', help='Jobs number input in this field')
    work_orders = fields.Char(string='Work Orders', help='Job work orders added in this field')
    # correction_reason = fields.Text(string="Correction Reason")
    aging_entry_days = fields.Integer(string="Aging For Entry", compute='_compute_aging_entry_days', store=True)
    aging_verification_days = fields.Integer(string="Aging For Verification", compute='_compute_aging_verification_date', store=True)


    pending_days = fields.Integer(
        string="Pending Days", readonly=True)

    @api.depends("create_date", "verification_datetime")
    def _compute_aging_entry_days(self):
        for record in self:
            if record.create_date and record.verification_datetime:
                delta = record.verification_datetime.date() - record.create_date.date()
                record.aging_entry_days = delta.days
            else:
                record.aging_entry_days = 0  # Default if any date is missing


    @api.depends('verification_datetime', 'done_datetime')
    def _compute_aging_verification_date(self):
        for rec in self:
            if rec.verification_datetime and rec.done_datetime:
                delta = rec.done_datetime.date() - rec.verification_datetime.date()
                rec.aging_verification_days = delta.days
            else:
                rec.aging_verification_days = 0 # set default 0

    @api.model
    def update_pending_days_daily(self):
        """
        Update pending days for all tickets daily.
        """
        tickets = self.search([('stage_id.name', '!=', 'Verification')])
        for ticket in tickets:
            if ticket.create_date:
                current_time = fields.Datetime.now()
                delta = current_time - ticket.create_date
                ticket.pending_days = delta.days

    # ---


    @api.onchange('team_id', 'team_head')
    def team_leader_domain(self):
        """Update the domain for the assigned user based on the selected team.

        This onchange method is triggered when the helpdesk team or team leader
        is changed. It updates the domain for the assigned user field to include
        only the members of the selected team."""
        teams = []
        for rec in self.team_id.member_ids:
            teams.append(rec.id)
        return {'domain': {'assigned_user': [('id', 'in', teams)]}}

    @api.depends('team_id')
    def _compute_team_head(self):
        """Compute the team head based on the selected team."""
        for record in self:
            record.team_head = record.team_id.team_lead_id.id if record.team_id else False

    @api.onchange('stage_id')
    def mail_snd(self):
        """Send an email when the stage of the ticket is changed.

        This onchange method is triggered when the stage of the ticket is
        changed. It updates the last update date, start date, and end date
        fields accordingly. If a template is associated with the stage, it
        sends an email using that template."""
        rec_id = self._origin.id
        data = self.env['help.ticket'].search([('id', '=', rec_id)])
        data.last_update_date = fields.Datetime.now()
        if self.stage_id.starting_stage:
            data.start_date = fields.Datetime.now()
        if self.stage_id.closing_stage or self.stage_id.cancel_stage:
            data.end_date = fields.Datetime.now()
        if self.stage_id.template_id:
            mail_template = self.stage_id.template_id
            mail_template.send_mail(self._origin.id, force_send=True)

    def assign_to_teamleader(self):
        """Assign the ticket to the team leader and send a notification.

        This function checks if a helpdesk team is selected and assigns the
        team leader to the ticket. It then sends a notification email to the
        team leader."""
        if self.team_id:
            self.team_head = self.team_id.team_lead_id.id
            mail_template = self.env.ref(
                'itl_it_ticketing.'
                'mail_template_itl_it_ticketing_assign')
                # 'mail_template_odoo_website_helpdesk_assign')
            mail_template.sudo().write({
                'email_to': self.team_head.email,
                'subject': self.name
            })
            mail_template.sudo().send_mail(self.id, force_send=True)
        else:
            raise ValidationError("Please choose a Helpdesk Team")

    def _default_show_create_task(self):
        """Get the default value for the 'show_create_task' field.

        This method retrieves the default value for the 'show_create_task'
        field from the configuration settings."""
        return self.env['ir.config_parameter'].sudo().get_param(
            'itl_it_ticketing.show_create_task')

    show_create_task = fields.Boolean(string="Show Create Task",
                                      default=_default_show_create_task,
                                      compute='_compute_show_create_task',
                                      help='Determines whether the Create Task'
                                           ' button should be shown for this '
                                           'ticket.')
    create_task = fields.Boolean(string="Create Task", readonly=False,
                                 related='team_id.create_task',
                                 store=True,
                                 help='Defines if a task should be created when'
                                      ' this ticket is created.')
    billable = fields.Boolean(string="Billable", help='Indicates whether the '
                                                      'ticket is billable or '
                                                      'not.')

    def _default_show_category(self):
        """Its display the default category"""
        return self.env['ir.config_parameter'].sudo().get_param(
            'itl_it_ticketing.show_category')

    show_category = fields.Boolean(default=_default_show_category,
                                   compute='_compute_show_category',
                                   help='Display the default category')
    customer_rating = fields.Selection(RATING, default='0',
                                       string='Customer Rating',
                                       help='Display the customer rating.')

    review = fields.Char(string='Review',
                         help='Customer review of the ticket.')
    kanban_state = fields.Selection([
        ('normal', 'Ready'),
        ('done', 'In Progress'),
        ('blocked', 'Blocked'), ], default='normal')

    ticket_from = fields.Selection([
        ('normal_create', 'Normal Create'),
        ('outgoing', 'Outgoing'),
        ('mail_create', 'Create From Mail')], default='normal_create')

    stage_id = fields.Many2one('ticket.stage', string='Stage',
                               default=lambda self: self.env[
                                   'ticket.stage'].search(
                                   [('name', '=', 'Draft')], limit=1).id,
                               tracking=True,
                               group_expand='_read_group_stage_ids',
                               help='Stages of the ticket.')

    is_verification_stage = fields.Boolean(
        string='Is Verification Stage',
        compute='_compute_is_verification_stage',
        store=True
    )

    @api.depends('stage_id')
    def _compute_is_verification_stage(self):
        """Compute whether the current stage is 'Verification'."""
        for record in self:
            record.is_verification_stage = record.stage_id.name == 'Verification'
    # Wizard update trace fields:
    updated_by = fields.Many2one(comodel_name='res.partner', string="Updated By")
    update_date = fields.Datetime(string="Update Time")
    update_reason = fields.Text(string="Update Reason")

    # stage base date field
    mis_datetime = fields.Datetime(string="MIS Date", readonly=True)
    cs_datetime = fields.Datetime(string="CS Date", readonly=True)
    in_progress_datetime = fields.Datetime(string="In Progress Date", readonly=True)
    verification_datetime = fields.Datetime(string="Verification Date", readonly=True)
    verified_by = fields.Many2one(comodel_name='res.users', string="Verified By", readonly=True)
    done_by = fields.Many2one(comodel_name='res.users', string="Done By", readonly=True)
    correction_by = fields.Many2one(comodel_name='res.users', string="Correction By", readonly=True)
    correction_datetime = fields.Datetime(string="Correction Date", readonly=True)
    done_datetime = fields.Datetime(string="Done Date", readonly=True)
    # --
    correction_info = fields.One2many('ticket.correction', 'ticket_id', string="Corrections")


    #---

    def _compute_show_category(self):
        """Compute show category"""
        show_category = self._default_show_category()
        for rec in self:
            rec.show_category = show_category

    def _compute_show_create_task(self):
        """Compute the value of the 'show_create_task' field for each record in
        the current recordset."""
        show_create_task = self._default_show_create_task()
        for record in self:
            record.show_create_task = show_create_task

    def auto_close_ticket(self):
        """Automatically closing the ticket based on the closing date."""
        auto_close = self.env['ir.config_parameter'].sudo().get_param(
            'itl_it_ticketing.auto_close_ticket')
        if auto_close:
            no_of_days = self.env['ir.config_parameter'].sudo().get_param(
                'itl_it_ticketing.no_of_days')
            records = self.env['help.ticket'].search([])
            for rec in records:
                days = (fields.Datetime.today() - rec.create_date).days
                if days >= int(no_of_days):
                    close_stage_id = self.env['ticket.stage'].search(
                        [('closing_stage', '=', True)])
                    if close_stage_id:
                        rec.stage_id = close_stage_id

    def default_stage_id(self):
        """Search your stage"""
        return self.env['ticket.stage'].search(
            [('name', '=', 'Draft')], limit=1).id

    @api.model
    def _read_group_stage_ids(self, stages, domain, order):
        """
        Return the available stages for grouping.

        This static method is used to provide the available stages for
        grouping when displaying records in a grouped view.

        """
        stage_ids = self.env['ticket.stage'].search([])
        return stage_ids



    @api.model
    def create(self, vals):
        """Override create to enforce unique subject and handle default values."""
        # Validate uniqueness of subject
        if 'subject' in vals and self.search([('subject', '=', vals['subject'])]):
            raise ValidationError("The ticket subject must be unique.")

        # Handle default values for name and description
        if not vals.get('subject'):
            vals['subject'] = vals['name']
        if vals.get('subject'):
            vals['name'] = self.env['ir.sequence'].next_by_code('help.ticket')
        else:
            vals['name'] = ''

        if not vals.get('description'):
            vals['description'] = 'Give your ticket description'
            vals['ticket_from'] = 'mail_create'

        return super(HelpTicket, self).create(vals)

    def write(self, vals):
        """Override write to handle unique subject and stage-based datetime updates."""

        # Validate uniqueness of subject
        if 'subject' in vals and self.search([('subject', '=', vals['subject']), ('id', '!=', self.id)]):
            raise ValidationError("The ticket subject must be unique.")

        # Handle stage-based datetime updates
        if 'stage_id' in vals:
            new_stage = self.env['ticket.stage'].browse(vals['stage_id'])
            current_time = fields.Datetime.now()

            for record in self:
                if new_stage.name == 'MIS':
                    vals['mis_datetime'] = current_time
                elif new_stage.name == 'CS':
                    vals['cs_datetime'] = current_time
                elif new_stage.name == 'In Progress':
                    vals['in_progress_datetime'] = current_time
                elif new_stage.name == 'Verification':
                    vals['verification_datetime'] = current_time
                    vals['verified_by'] = self.env.user.id  # Set current user
                elif new_stage.name == 'Correction':
                    vals['correction_datetime'] = current_time
                    vals['correction_by'] = self.env.user.id  # Set current user
                elif new_stage.name == 'Done':
                    vals['done_datetime'] = current_time
                    vals['done_by'] = self.env.user.id  # Set current user
        # Handle the correction stage notification
        if 'stage_id' in vals:
            correction_stage = self.env['ticket.stage'].search([('name', '=', 'Correction')], limit=1)
            if vals['stage_id'] == correction_stage.id:
                # Allow stage update only if bypass_correction_notification is set in the context
                if not self.env.context.get('bypass_correction_notification', False):
                    raise ValidationError("Please click the Correction button to convert to the Correction stage.")

        return super(HelpTicket, self).write(vals)

    def btn_assign_me_action(self):
        """
        Automatically assign the current user to the ticket and, if applicable,
        their associated helpdesk team and team leader.
        """
        for record in self:
            current_user = self.env.user

            # Assign the current user to the ticket
            record.assigned_user = [(4, current_user.id)]

            # Check if the current user belongs to a helpdesk team
            team = self.env['help.team'].search([('member_ids', '=', current_user.id)], limit=1)
            if team:
                record.team_id = team.id

                # Assign the team leader if available
                if team.team_lead_id:
                    record.team_head = team.team_lead_id.id
                else:
                    record.team_head = False  # Clear team_head if no team leader found
            else:
                # Clear team and team_head if no team found
                record.team_id = False
                record.team_head = False

    def action_create_invoice(self):
        """Create Invoice for Help Desk Ticket.
        This function creates an invoice for the help desk ticket based on
        the associated tasks with billed hours.
        """
        tasks = self.env['project.task'].search(
            [('project_id', '=', self.project_id.id),
             ('ticket_id', '=', self.id)]).filtered(
            lambda line: line.ticket_billed == True)
        if not tasks:
            raise UserError('No Tasks to Bill')
        total = sum(x.effective_hours for x in tasks if x.effective_hours > 0)
        invoice_no = self.env['ir.sequence'].next_by_code(
            'ticket.invoice')
        self.env['account.move'].create([
            {
                'name': invoice_no,
                'move_type': 'out_invoice',
                'partner_id': self.customer_id.id,
                'ticket_id': self.id,
                'date': fields.Date.today(),
                'invoice_date': fields.Date.today(),
                'invoice_line_ids':
                    [(0, 0, {'product_id': self.service_product_id.id,
                             'name': self.service_product_id.name,
                             'quantity': total,
                             'product_uom_id': self.service_product_id.uom_id.id,
                             'price_unit': self.cost,
                             'account_id':
                                 self.service_product_id.categ_id.property_account_income_categ_id.id,
                             })],
            }, ])
        for task in tasks:
            task.ticket_billed = True
        return {
            'effect': {
                'fadeout': 'medium',
                'message': 'Billed Successfully!',
                'type': 'rainbow_man',
            }
        }

    def action_create_tasks(self):
        """Create Task for HelpDesk Ticket
        This function creates a task associated with the helpdesk ticket
        and updates the task_ids field.
        """
        task_id = self.env['project.task'].create({
            'name': self.name + '-' + self.subject,
            'project_id': self.project_id.id,
            'company_id': self.env.company.id,
            'ticket_id': self.id,
        })
        self.write({
            'task_ids': [(4, task_id.id)]
        })
        return {
            'name': 'Tasks',
            'res_model': 'project.task',
            'view_id': False,
            'res_id': task_id.id,
            'view_mode': 'form',
            'type': 'ir.actions.act_window',
            'target': 'new',
        }

    def action_open_tasks(self):
        """Smart Button of Task to view the Tasks of HelpDesk Ticket"""
        return {
            'name': 'Tasks',
            'domain': [('ticket_id', '=', self.id)],
            'res_model': 'project.task',
            'view_id': False,
            'view_mode': 'tree,form',
            'type': 'ir.actions.act_window',
        }

    def action_open_invoices(self):
        """Smart Button of Invoice to view the Invoices for HelpDesk Ticket"""
        return {
            'name': 'Invoice',
            'domain': [('ticket_id', '=', self.id)],
            'res_model': 'account.move',
            'view_id': False,
            'view_mode': 'tree,form',
            'type': 'ir.actions.act_window',
        }

    def action_open_merged_tickets(self):
        """ Smart button of the merged tickets"""
        ticket_ids = self.env['support.tickets'].search(
            [('merged_ticket', '=', self.id)])
        # Get the display_name matching records from the support.tickets
        helpdesk_ticket_ids = ticket_ids.mapped('display_name')
        # Get the IDs of the help.ticket records matching the display names
        help_ticket_records = self.env['help.ticket'].search(
            [('name', 'in', helpdesk_ticket_ids)])
        return {
            'type': 'ir.actions.act_window',
            'name': 'Helpdesk Ticket',
            'view_mode': 'tree,form',
            'res_model': 'help.ticket',
            'domain': [('id', 'in', help_ticket_records.ids)],
            'context': self.env.context,
        }

    def action_send_reply(self):
        """Compose and send a reply to the customer.
        This function opens a window for composing and sending a reply to
        the customer. It uses the configured email template for replies.
       """
        template_id = self.env['ir.config_parameter'].sudo().get_param(
            'itl_it_ticketing.reply_template_id'
        )
        template_id = self.env['mail.template'].browse(int(template_id))
        if template_id:
            return {
                'type': 'ir.actions.act_window',
                'name': 'mail',
                'res_model': 'mail.compose.message',
                'view_mode': 'form',
                'target': 'new',
                'views': [[False, 'form']],
                'context': {
                    'default_model': 'help.ticket',
                    'default_res_id': self.id,
                    'default_template_id': template_id.id
                }
            }
        return {
            'type': 'ir.actions.act_window',
            'name': 'mail',
            'res_model': 'mail.compose.message',
            'view_mode': 'form',
            'target': 'new',
            'views': [[False, 'form']],
            'context': {
                'default_model': 'help.ticket',
                'default_res_id': self.id,
            }
        }

    def btn_correction_ticket(self):
        """Show the Correction form and pre-fill default values."""
        self.ensure_one()  # Ensures the method acts on a single record
        if self.stage_id.name == 'Correction':  # Ensure this comparison checks the stage name
            raise ValidationError("This Ticket is Already in Correction Stage!")

        return {
            'type': 'ir.actions.act_window',
            'name': 'Ticket Correction',
            'view_mode': 'form',
            'res_model': 'ticket.correction',
            'target': 'new',  # Open in a modal
            'context': {
                'default_ticket_id': self.id,
                'default_correction_date': fields.Date.today(),
            }
        }

    def btn_multiple_ticket_stage_updates(self):
        """Multiple Tickets Stage Update Dynamically"""
        # Get selected ticket IDs from the context
        selected_tickets = self.env.context.get('active_ids', [])

        if not selected_tickets:
            raise UserError("No tickets selected for stage update.")

        return {
            'type': 'ir.actions.act_window',
            'name': 'Multiple Ticket Stage Updates',
            'view_mode': 'form',
            'view_id': self.env.ref('itl_it_ticketing.update_ticket_stage_form_view').id,
            'res_model': 'ticket.update.wizard',
            'target': 'new',
            'context': {
                'default_ticket_ids': [(6, 0, selected_tickets)],  # Set default selected tickets
            }
        }

    def action_download_attachment(self):
        """Download all non-image attachments of the current Help Ticket."""
        self.ensure_one()  # Ensure the method is called on a single record

        # Search for attachments related to the current ticket
        attachments = self.env['ir.attachment'].search([
            ('res_model', '=', 'help.ticket'),
            ('res_id', '=', self.id),
            ('mimetype', 'not ilike', 'image/png'),  # Exclude .png
            ('mimetype', 'not ilike', 'image/jpeg'),  # Exclude .jpeg
            ('mimetype', 'not ilike', 'image/jpg'),  # Exclude .jpg
        ])

        if not attachments:
            raise ValidationError("No non-image attachments found for this ticket.")
        else:
            # Generate the URL for downloading the filtered attachments
            url = '/web/binary/download_document?tab_id=%s' % ','.join(map(str, attachments.ids))
            return {
                'type': 'ir.actions.act_url',
                'url': url,
                'target': 'new',
            }

