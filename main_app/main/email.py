from flask.templating import render_template, current_app
from flask_mail import Message
from threading import Thread
from main_app import mail
from dotenv import load_dotenv
import os

load_dotenv()

MAIL_SUBJECT_PREFIX = os.getenv('MAIN_MAIL_SUBJECT_PREFIX')
MAIL_SENDER = os.getenv('MAIN_MAIL_USERNAME')


def send_async_email(app, msg):
    with app.app_context():
        mail.send(msg)


def send_email(to, subject, template, **kwargs):
    app = current_app._get_current_object()
  
    msg = Message(MAIL_SUBJECT_PREFIX + subject,
                  sender=MAIL_SENDER, recipients=to)
    msg.html = render_template(template + '.html', **kwargs)
    thr = Thread(target=send_async_email, args=[app, msg])
    thr.start()
    return thr