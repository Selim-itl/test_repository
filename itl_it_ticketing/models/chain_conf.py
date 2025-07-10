# ITL Bangladesh Limited
from odoo import fields, models, api
from odoo.exceptions import UserError


class ChainConfigurations(models.Model):
    _name = 'it.itl.bd.chain.conf'
    _description = 'Product Chain'
    _rec_name = 'name'

    name = fields.Char(string="Chain Name")
    chain_ids = fields.Char(string="Chain IDs")
    chain_description = fields.Char(string="Description")
    chain_address = fields.Char(string="Chain Address")

    # def name_get(self):
    #     res = []
    #     for record in self:
    #         res.append((record.id, f"{record.name} {'/'} {record.chain_ids or 'ITL'}"))
    #     return res

