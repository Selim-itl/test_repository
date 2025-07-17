import base64
import io
import logging
import pandas as pd
import chardet
from datetime import datetime
from odoo.exceptions import ValidationError
from odoo import models, fields, _

_logger = logging.getLogger(__name__)

class ImportHelpTicket(models.TransientModel):
    _name = 'it.itl.bd.import.help.ticket'
    _description = 'Import Help Ticket Data'

    file_type = fields.Selection([('CSV', 'CSV File'), ('XLS', 'XLS File')], string='File Type', default='XLS')
    file = fields.Binary(string="Upload File")

    def btn_help_ticket_data_func(self):
        """Handles the import of Help Ticket data from Excel or CSV files."""
        if not self.file:
            raise ValidationError(_("Please upload a file to import Help Ticket data!"))

        try:
            decoded_file = base64.b64decode(self.file)

            # Detect file encoding
            result = chardet.detect(decoded_file)
            encoding = result['encoding']

            # Read file into Pandas DataFrame
            file_stream = io.BytesIO(decoded_file)
            df = pd.read_excel(file_stream, engine='openpyxl') if self.file_type == 'XLS' else pd.read_csv(file_stream, encoding=encoding)

            # Convert all columns to string safely
            df = df.astype(str).replace("nan", "", regex=True)

            # Check for required columns
            required_columns = ["Create By", "Customer Name", "Stage", "Select Chain", "Ticket Owner", "Subject"]
            missing_columns = [col for col in required_columns if col not in df.columns]
            if missing_columns:
                raise ValidationError(_("Missing columns: %s") % ", ".join(missing_columns))

            batch_size = 1000
            records = df.to_dict(orient='records')
            batch = []

            for record in records:
                batch.append(record)
                if len(batch) >= batch_size:
                    self.process_batch(batch)
                    batch = []

            if batch:
                self.process_batch(batch)

        except Exception as e:
            _logger.error("Error while importing file: %s", str(e))
            raise ValidationError(_("Error while importing file. Check log for details."))

        return {
            'type': 'ir.actions.client',
            'tag': 'display_notification',
            'params': {
                'title': _('Import Result'),
                'message': _('Your Help Ticket Data has been successfully uploaded!'),
                'type': 'success',
                'sticky': False,
            }
        }

    def process_batch(self, batch):
        """Processes a batch of help tickets ensuring relational fields are correctly handled."""
        with self.env.cr.savepoint():
            existing_tickets = {}
            new_tickets = []

            # Extract unique names for relational lookups
            user_names = set(str(rec["Create By"]).strip() for rec in batch if rec["Create By"])
            customer_names = set(str(rec["Customer Name"]).strip() for rec in batch if rec["Customer Name"])
            stage_names = set(str(rec["Stage"]).strip() for rec in batch if rec["Stage"])
            chain_names = set(str(rec["Select Chain"]).strip() for rec in batch if rec["Select Chain"])
            assigned_users = set(str(rec["Ticket Owner"]).strip() for rec in batch if rec["Ticket Owner"])

            # Fetch relational records in bulk
            users = {user.name: user for user in self.env['res.users'].search([('name', 'in', list(user_names))])}
            customers = {customer.name: customer for customer in
                         self.env['res.partner'].search([('name', 'in', list(customer_names))])}
            stages = {stage.name: stage for stage in
                      self.env['it.itl.bd.ticket.stage'].search([('name', 'in', list(stage_names))])}
            chains = {chain.name: chain for chain in self.env['it.itl.bd.chain.conf'].search([('name', 'in', list(chain_names))])}
            assigned_users_dict = {user.name: user for user in
                                   self.env['res.users'].search([('name', 'in', list(assigned_users))])}

            # Fetch existing tickets by subject and customer
            ticket_subjects = set(str(rec["Subject"]).strip() for rec in batch if rec["Subject"])
            existing_tickets_db = self.env['it.itl.bd.help.ticket'].search([('subject', 'in', list(ticket_subjects))])
            existing_ticket_map = {(ticket.subject, ticket.customer_id.id): ticket for ticket in existing_tickets_db}

            # Process each record in the batch
            for rec in batch:
                user_name = str(rec.get("Create By", "")).strip()
                customer_name = str(rec.get("Customer Name", "")).strip()
                stage_name = str(rec.get("Stage", "")).strip()
                chain_name = str(rec.get("Select Chain", "")).strip()
                assigned_user_names = str(rec.get("Ticket Owner", "")).strip().split(',')
                subject = str(rec.get("Subject", "")).strip()

                # Get or create User safely
                user = users.get(user_name)
                if not user:
                    unique_login = user_name.replace(" ", "_").lower()
                    existing_user = self.env['res.users'].search([('login', '=', unique_login)], limit=1)
                    if existing_user:
                        unique_login = f"{unique_login}_{int(datetime.timestamp(datetime.now()))}"
                    user = self.env['res.users'].create({'name': user_name, 'login': unique_login})
                    users[user_name] = user

                # Debugging: Check if we have user and its id
                _logger.info(f"User: {user_name} -> ID: {user.id if user else 'Not found'}")

                # Get or create Customer safely
                customer = customers.get(customer_name)
                if not customer:
                    customer = self.env['res.partner'].create({'name': customer_name})
                    customers[customer_name] = customer

                # Debugging: Check if we have customer and its id
                _logger.info(f"Customer: {customer_name} -> ID: {customer.id if customer else 'Not found'}")

                # Get or create Stage safely
                stage = stages.get(stage_name)
                if not stage:
                    stage = self.env['it.itl.bd.ticket.stage'].create({'name': stage_name})
                    stages[stage_name] = stage

                # Debugging: Check if we have stage and its id
                _logger.info(f"Stage: {stage_name} -> ID: {stage.id if stage else 'Not found'}")

                # Get or create Chain safely
                chain_ids = []
                for name in chain_name.split(','):
                    name = name.strip()
                    if name:
                        chain = chains.get(name)
                        if not chain:
                            chain = self.env['it.itl.bd.chain.conf'].create({'name': name})
                            chains[name] = chain
                        chain_ids.append(chain.id)

                # Debugging: Check if we have chain ids
                _logger.info(f"Chain IDs: {chain_ids}")

                # Get Assigned Users (Many2many) safely
                assigned_user_ids = []
                for name in assigned_user_names:
                    name = name.strip()
                    if name:
                        assigned_user = assigned_users_dict.get(name)
                        if not assigned_user:
                            unique_login = name.replace(" ", "_").lower()
                            existing_user = self.env['res.users'].search([('login', '=', unique_login)], limit=1)
                            if existing_user:
                                unique_login = f"{unique_login}_{int(datetime.timestamp(datetime.now()))}"
                            assigned_user = self.env['res.users'].create({'name': name, 'login': unique_login})
                            assigned_users_dict[name] = assigned_user
                        assigned_user_ids.append(assigned_user.id)

                # Ensure Unique Ticket Subject (Add Timestamp)
                unique_subject = subject
                if (subject, customer.id) in existing_ticket_map:
                    unique_subject = f"{subject} - {datetime.now().strftime('%Y%m%d%H%M%S')}"

                # Prepare ticket data
                ticket_values = {
                    'user_id': user.id if user else False,
                    'customer_id': customer.id if customer else False,
                    'stage_id': stage.id if stage else False,
                    'chain_ids': [(6, 0, chain_ids)],
                    'assigned_user': [(6, 0, assigned_user_ids)],
                    'subject': unique_subject,
                }

                # Check if ticket exists before creating
                existing_ticket = existing_ticket_map.get((unique_subject, customer.id))
                if existing_ticket:
                    existing_tickets[existing_ticket.id] = ticket_values
                else:
                    new_tickets.append(ticket_values)
                    existing_ticket_map[(unique_subject, customer.id)] = True  # Mark as used

            # Update existing tickets
            for ticket_id, values in existing_tickets.items():
                self.env['it.itl.bd.help.ticket'].browse(ticket_id).write(values)

            # Create new tickets
            if new_tickets:
                self.env['it.itl.bd.help.ticket'].create(new_tickets)


