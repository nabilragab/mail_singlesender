# Part of Odoo. See LICENSE file for full copyright and licensing details.

import logging
from odoo import _, api, models, tools
from odoo.exceptions import UserError

_logger = logging.getLogger(__name__)


# MODIFICATION HERE:
class Message(models.Model):
    """ Messages model: system notification (replacing res.log notifications),
        comments (OpenChatter discussion) and incoming emails. """
    _inherit = 'mail.message'
    @api.model
    def _get_default_from(self):
        if self.env.user.email:
            # MODIFICATION HERE
            return tools.formataddr((self.env.user.name,
                                     self.env["ir.config_parameter"].sudo().get_param("single.sender.email")))
        raise UserError(_("Unable to post message, please configure the sender's email address."))
