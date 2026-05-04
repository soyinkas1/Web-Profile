"""
Contact form with layered anti-abuse defences.

Defence order (cheapest to most expensive, fail-fast):
    1. Honeypot fields              -> kills naive bots
    2. Submission timing            -> kills fast bots
    3. Header-injection guard       -> kills SMTP relay attempts
    4. Content heuristics           -> kills gibberish + link spam
    5. Disposable-domain blocklist  -> reduces throwaway abuse

Rate limiting and CAPTCHA live at the route layer.
"""

import re
import time
import logging
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField, HiddenField
from wtforms.validators import DataRequired, Email, Length, ValidationError

logger = logging.getLogger(__name__)

MIN_FILL_SECONDS = 3
MAX_FORM_AGE_SECONDS = 60 * 60

DISPOSABLE_DOMAINS = frozenset({
    "mailinator.com", "guerrillamail.com", "10minutemail.com",
    "tempmail.com", "throwaway.email", "yopmail.com", "trashmail.com",
    "sharklasers.com", "getairmail.com", "maildrop.cc",
})

_CONSONANT_RUN = re.compile(r"[bcdfghjklmnpqrstvwxz]{5,}", re.IGNORECASE)
_URL_PATTERN = re.compile(r"https?://\S+", re.IGNORECASE)
_CRLF_NULL = ("\r", "\n", "\0")


def _looks_like_gibberish(text):
    text = text.strip()
    if not text:
        return False
    if _CONSONANT_RUN.search(text):
        return True
    letters = [c for c in text.lower() if c.isalpha()]
    if len(letters) >= 6:
        vowel_ratio = sum(1 for c in letters if c in "aeiou") / len(letters)
        if vowel_ratio < 0.15:
            return True
    return False


def _has_header_injection(value):
    return any(c in value for c in _CRLF_NULL)


class WebForm(FlaskForm):
    name = StringField(
        validators=[DataRequired(), Length(min=2, max=80)],
        render_kw={"placeholder": "Your Name", "maxlength": 80, "autocomplete": "name"},
    )
    email = StringField(
        validators=[DataRequired(), Email(), Length(max=120)],
        render_kw={"placeholder": "Your email", "maxlength": 120, "autocomplete": "email"},
    )
    subject = StringField(
        validators=[DataRequired(), Length(min=2, max=150)],
        render_kw={"placeholder": "Subject", "maxlength": 150},
    )
    message = TextAreaField(
        validators=[DataRequired(), Length(min=20, max=2000)],
        render_kw={"rows": 7, "placeholder": "Message", "maxlength": 2000},
    )

    # Honeypots: hidden in template, must remain empty
    website = HiddenField()
    phone_number = HiddenField()
    # Set by the GET handler in views.py
    form_loaded_at = HiddenField()

    submit = SubmitField("Send Message")

    def validate_website(self, field):
        if field.data:
            logger.warning("Honeypot 'website' triggered")
            raise ValidationError("Spam detected.")

    def validate_phone_number(self, field):
        if field.data:
            logger.warning("Honeypot 'phone_number' triggered")
            raise ValidationError("Spam detected.")

    def validate_form_loaded_at(self, field):
        try:
            loaded = float(field.data)
        except (TypeError, ValueError):
            raise ValidationError("Invalid submission. Please reload and try again.")
        elapsed = time.time() - loaded
        if elapsed < MIN_FILL_SECONDS:
            logger.warning("Form submitted in %.2fs (bot-like)", elapsed)
            raise ValidationError("Submitted too quickly. Please try again.")
        if elapsed > MAX_FORM_AGE_SECONDS:
            raise ValidationError("Form expired. Please reload and try again.")

    def validate_name(self, field):
        if _has_header_injection(field.data):
            logger.warning("Header-injection attempt in name field")
            raise ValidationError("Invalid characters in name.")
        if _looks_like_gibberish(field.data):
            raise ValidationError("Please enter a valid name.")

    def validate_subject(self, field):
        if _has_header_injection(field.data):
            logger.warning("Header-injection attempt in subject field")
            raise ValidationError("Invalid characters in subject.")
        if _looks_like_gibberish(field.data):
            raise ValidationError("Please enter a valid subject.")

    def validate_email(self, field):
        domain = field.data.rsplit("@", 1)[-1].lower()
        if domain in DISPOSABLE_DOMAINS:
            raise ValidationError("Please use a permanent email address.")

    def validate_message(self, field):
        if len(_URL_PATTERN.findall(field.data)) > 2:
            raise ValidationError("Too many links in message.")