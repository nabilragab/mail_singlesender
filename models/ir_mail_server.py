from odoo import _

from odoo.addons.base.models.ir_mail_server import *

_logger = logging.getLogger(__name__)
_test_logger = logging.getLogger('odoo.tests')

SMTP_TIMEOUT = 60


class IrMailServer(models.Model):
    _inherit = "ir.mail_server"

    @api.model
    def _get_default_from_address(self):
        """Compute the default from address.

        Used for the "header from" address when no other has been received.

        :return str/None:
            If the config parameter ``mail.default.from`` contains
            a full email address, return it.
            Otherwise, combines config parameters ``mail.default.from`` and
            ``mail.catchall.domain`` to generate a default sender address.

            If some of those parameters is not defined, it will default to the
            ``--email-from`` CLI/config parameter.
        """
        get_param = self.env['ir.config_parameter'].sudo().get_param
        # TODO: MODIFICATION HERE: self.single_sender_email_rfc
        # email_from = get_param("mail.default.from")
        email_from = get_param("single.sender.email.rfc")

        if email_from and "@" in email_from:
            return email_from
        domain = get_param("mail.catchall.domain")
        if email_from and domain:
            return "%s" % email_from
        return tools.config.get("email_from")

    def _prepare_email_message(self, message, smtp_session):
        """Prepare the SMTP information (from, to, message) before sending.

        :param message: the email.message.Message to send, information like the
            Return-Path, the From, etc... will be used to find the smtp_from and to smtp_to
        :param smtp_session: the opened SMTP session to use to authenticate the sender
        :return: smtp_from, smtp_to_list, message
            smtp_from: email to used during the authentication to the mail server
            smtp_to_list: list of email address which will receive the email
            message: the email.message.Message to send
        """
        # Use the default bounce address **only if** no Return-Path was
        # provided by caller.  Caller may be using Variable Envelope Return
        # Path (VERP) to detect no-longer valid email addresses.
        bounce_address = message['Return-Path'] or self._get_default_bounce_address() or message['From']
        smtp_from = message['From'] or bounce_address
        assert smtp_from, "The Return-Path or From header is required for any outbound email"

        email_to = message['To']
        email_cc = message['Cc']
        email_bcc = message['Bcc']
        del message['Bcc']

        # All recipient addresses must only contain ASCII characters
        smtp_to_list = [
            address
            for base in [email_to, email_cc, email_bcc]
            for address in extract_rfc2822_addresses(base)
            if address
        ]
        assert smtp_to_list, self.NO_VALID_RECIPIENT

        x_forge_to = message['X-Forge-To']
        if x_forge_to:
            # `To:` header forged, e.g. for posting on mail.channels, to avoid confusion
            del message['X-Forge-To']
            del message['To']           # avoid multiple To: headers!
            message['To'] = x_forge_to

        # Try to not spoof the mail from headers
        from_filter = getattr(smtp_session, 'from_filter', False)
        smtp_from = getattr(smtp_session, 'smtp_from', False) or smtp_from

        notifications_email = email_normalize(self._get_default_from_address())
        if notifications_email and smtp_from == notifications_email and message['From'] != notifications_email:
            smtp_from = encapsulate_email(message['From'], notifications_email)

        if message['From'] != smtp_from:
            del message['From']
            message['From'] = smtp_from

        # Check if it's still possible to put the bounce address as smtp_from
        if self._match_from_filter(bounce_address, from_filter):
            # Mail headers FROM will be spoofed to be able to receive bounce notifications
            # Because the mail server support the domain of the bounce address
            smtp_from = bounce_address

        # The email's "Envelope From" (Return-Path) must only contain ASCII characters.
        smtp_from_rfc2822 = extract_rfc2822_addresses(smtp_from)
        assert smtp_from_rfc2822, (
            f"Malformed 'Return-Path' or 'From' address: {smtp_from} - "
            "It should contain one valid plain ASCII email")
        # TODO: MODIFICATION HERE: self.single_sender_email_rfc
        smtp_from = self.env["ir.config_parameter"].sudo().get_param("single.sender.email.rfc")
        # smtp_from = smtp_from_rfc2822[-1]
        return smtp_from, smtp_to_list, message
