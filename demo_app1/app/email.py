from flask.templating import render_template, current_app
from flask_mail import Message
from threading import Thread
from demo_app1.app.extensions import mail
from dotenv import load_dotenv
import os
import logging

load_dotenv()

MAIL_SUBJECT_PREFIX = os.getenv('DEMO1_MAIL_SUBJECT_PREFIX')
MAIL_SENDER = os.getenv('DEMO1_MAIL_USERNAME')

# Disable Flask-Mail logging (if any)
logging.getLogger('flask_mail').setLevel(logging.CRITICAL)

# Disable smtplib logs
logging.getLogger('smtplib').setLevel(logging.CRITICAL)


def send_async_email(app, msg):
    with app.app_context():
        mail.send(msg)


def send_email(to, subject, template, **kwargs):
    app = current_app._get_current_object()
    
    msg = Message(MAIL_SUBJECT_PREFIX + subject,
                  sender=MAIL_SENDER, recipients=[to])
    msg.html = render_template(template + '.html', **kwargs)
    thr = Thread(target=send_async_email, args=[app, msg])
    thr.start()
    return thr