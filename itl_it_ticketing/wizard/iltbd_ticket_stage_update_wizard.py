from odoo import models, fields, api
from odoo.exceptions import UserError


class SelectedTicketStageUpdate(models.Model):
    _name = 'it.itl.bd.ticket.update.wizard'
    _description = 'Multiple Ticket Stage Update'

    ticket_ids = fields.Many2many(comodel_name='it.itl.bd.help.ticket', string='Tickets', readonly=True)
    updated_by = fields.Many2one(comodel_name='res.partner', string="Updated By",readonly=True,
                                 default=lambda self: self.env.user.partner_id)
    update_date = fields.Datetime(string="Update Time", default=fields.Datetime.now, readonly=True)
    stage_id = fields.Many2one(
        'it.itl.bd.ticket.stage',
        string='Stage',
        required=True,
        help='Stages of the ticket.',
        domain=[('name', '!=', 'Correction')]  # Exclude "Correction" stage
    )
    update_reason = fields.Text(string="Update Reason")

    def btn_update_ticket_stage_action(self):
        # Ensure tickets are selected
        if not self.ticket_ids:
            raise UserError("No tickets selected for stage update.")

        # Collect ticket references for logging
        updated_ticket_refs = []

        for wizard in self:
            for ticket in wizard.ticket_ids:
                # Update the ticket with new stage and other details
                ticket.write({
                    'stage_id': wizard.stage_id.id,
                    'updated_by': wizard.updated_by.id,
                    'update_date': wizard.update_date,
                    'update_reason': wizard.update_reason,
                })
                updated_ticket_refs.append(ticket.name)

        # Display a confirmation message with updated ticket references
        # ticket_list = ", ".join(updated_ticket_refs)

        # Return the action to show the notification and close the wizard
        # return {
        #     'type': 'ir.actions.client',
        #     'tag': 'display_notification',
        #     'params': {
        #         'title': 'Tickets Updated Successfully',
        #         'message': f"The following tickets were updated: {ticket_list}",
        #         'sticky': False,
        #     },
        #     # Close the wizard window after the update
        #     'window_close': True,
        # }

