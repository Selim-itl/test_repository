from odoo import fields, models, api
from odoo.tools import datetime

from odoo.exceptions import ValidationError

from odoo import exceptions
from odoo.exceptions import UserError


class TicketCorrectionModel(models.Model):
    _name = 'ticket.correction'
    _rec_name = 'name'
    _description = 'All Correction Ticket Records'


    name = fields.Char(string="Correction ID.")
    ticket_id = fields.Many2one('help.ticket', string='Ticket NO.')
    correction_date = fields.Date(string='Correction Date',readonly=True, default=fields.Date.today())
    correction_reason = fields.Text(string="Correction Description")
    correction_by = fields.Many2one('res.users', 'Checked By',readonly=True, default=lambda self: self.env.user)
    # state = fields.Selection([('correction', 'Correction')], "State")



    # @api.model
    # def create(self, vals_list):
    #     # Ensure the method handles multiple records in batch
    #     records = super().create(vals_list)
    #     for record in records:
    #         name_text = f'TK/Cr/ID-0000101{record.id}'
    #         record.update({'name': name_text})
    #     return records

    @api.model
    def create(self, vals_list):
        # Create the records in batch
        records = super().create(vals_list)

        # Update the 'name' field for each record in the batch
        for record in records:
            name_text = f'TK/Cr/ID-0000101{record.id}'
            record.name = name_text

        return records

    def btn_correction_ticket_submit(self):
        """Save correction details and update the related ticket."""
        self.ensure_one()

        if not self.ticket_id:
            raise ValidationError("No associated ticket found for this correction.")

        # Get the "Correction" stage
        correction_stage = self.env['ticket.stage'].search([('name', '=', 'Correction')], limit=1)
        if not correction_stage:
            raise ValidationError("Correction stage is not configured. Please contact your administrator.")

        # Add this correction to the ticket and update its stage
        with self.env.cr.savepoint():
            self.ticket_id.with_context(bypass_correction_notification=True).write({
                'correction_info': [(4, self.id)],  # Link this correction record
                'stage_id': correction_stage.id  # Update ticket stage to "Correction"
            })












