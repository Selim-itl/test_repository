# -*- coding: utf-8 -*-
#############################################################################
#
#    ITL Bangladesh Limited
#
#############################################################################
from odoo import fields, models


class HelpdeskTag(models.Model):
    """ Its handle to control the helpdesk ticket tags"""
    _name = 'it.itl.bd.helpdesk.tag'
    _description = 'Helpdesk Tag'

    name = fields.Char(string='Tag', help='Choose the tags')
