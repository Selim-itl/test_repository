# -*- coding: utf-8 -*-
#############################################################################
#
#    ITL Bangladesh Limited
#
#############################################################################
from odoo import models


class WebsiteMenu(models.Model):
    """
     Inheriting the website menu.

     This class inherits from the 'website.menu' model and extends its
     functionality to compute the visibility of the menu
     item based on the value of the 'itl_it_ticketing.helpdesk_menu_show'
     configuration parameter.

     Attributes:
        _inherit (str): The name of the model being inherited.
    """
    _inherit = "website.menu"

    def _compute_visible(self):
        """
        Compute the visibility of the menu item.

        This method is used to determine whether the menu item should be
        visible or hidden based on the value of the
        'itl_it_ticketing.helpdesk_menu_show' configuration parameter.

        Returns:
            None

        Side Effects:
            Sets the 'is_visible' field of the menu item record to True or
            False accordingly.
        """
        super()._compute_visible()
        show_menu_header = self.env['ir.config_parameter'].sudo().get_param(
            'itl_it_ticketing.helpdesk_menu_show')
        for menu in self:
            if menu.name == 'Helpdesk' and show_menu_header is False:
                menu.is_visible = False
            if menu.name == 'Helpdesk' and show_menu_header is True:
                menu.is_visible = True
