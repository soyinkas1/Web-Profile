"""
Email dispatch for the contact form.

Hardened against:
  - SMTP relay abuse: recipients are hard-coded to the site owner.
    User-supplied email goes into Reply-To (a single structured header),
    never into the To/Cc/Bcc list.
  - Header injection: CR/LF/NUL stripped from any value that flows
    into a header (subject, sender name, reply-to address).
"""

import os
import re
import logging
from threading import Thread

from flask import current_app
from flask.templating import render_template
from flask_mail import Message
from dotenv import load_dotenv

from main_app import mail

load_dotenv()
logger = logging.getLogger(__name__)

MAIL_SUBJECT_PREFIX = os.getenv("MAIN_MAIL_SUBJECT_PREFIX", "")
MAIL_SENDER = os.getenv("MAIN_MAIL_USERNAME")

# Strip CR/LF/NUL from any value that flows into mail headers.
# These characters allow header injection — a single newline in
# "subject" can let an attacker inject Bcc:, From:, or other headers.
_HEADER_UNSAFE = re.compile(r"[\r\n\0]")


def _sanitise_header(value, max_len=200):
    """Remove characters that could break out of a mail header."""
    if not value:
        return ""
    return _HEADER_UNSAFE.sub(" ", str(value))[:max_len].strip()


def _send_async_email(app, msg):
    """Send the message inside an app context. Log failures, don't crash."""
    with app.app_context():
        try:
            mail.send(msg)
            logger.info("Mail sent to %s", msg.recipients)
        except Exception:
            logger.exception("Async mail send failed")


def send_contact_notification(sender_name, sender_email, subject, message_body):
    """
    Send a contact-form submission to the site owner ONLY.

    The user-supplied email is set as Reply-To (safe — it's a single
    structured header), never as a recipient. This prevents the form
    from being abused as an SMTP relay to deliver spam to third parties.

    Args:
        sender_name: Submitter's name (from form, untrusted)
        sender_email: Submitter's email (from form, untrusted)
        subject:     Subject line (from form, untrusted)
        message_body: Free-form message (from form, untrusted)

    Returns:
        The Thread running the async send (mostly for testing).
    """
    app = current_app._get_current_object()

    safe_subject = _sanitise_header(subject, max_len=150)
    safe_name = _sanitise_header(sender_name, max_len=80)
    safe_reply_to = _sanitise_header(sender_email, max_len=120)

    msg = Message(
        subject=f"{MAIL_SUBJECT_PREFIX}{safe_subject}",
        sender=MAIL_SENDER,            # always your own verified address
        recipients=[MAIL_SENDER],      # ONLY ever sent to you
        reply_to=safe_reply_to,        # clicking Reply goes to the sender
    )
    msg.html = render_template(
        "mail.html",
        name=safe_name,
        message=message_body,          # body content, not a header
    )

    thr = Thread(target=_send_async_email, args=[app, msg])
    thr.start()
    return thr


# --- Backward-compatibility shim ---------------------------------------
#
# The original send_email(to, subject, template, **kwargs) signature is
# kept temporarily so any callers we haven't updated yet don't break at
# import time. It now ROUTES THROUGH send_contact_notification, ignoring
# the caller's `to` argument — preventing the relay even if a caller
# passes a user-supplied address. Remove this shim once views.py has
# been updated and you've grepped the codebase for any other callers.
def send_email(to, subject, template, **kwargs):
    logger.warning(
        "Deprecated send_email() called — routing to send_contact_notification. "
        "Caller-supplied recipients %r ignored for security.", to,
    )
    return send_contact_notification(
        sender_name=kwargs.get("name", ""),
        sender_email=to[1] if isinstance(to, (list, tuple)) and len(to) > 1 else "",
        subject=subject,
        message_body=kwargs.get("message", ""),
    )