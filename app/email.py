import time
from threading import Thread

import celery
from flask import render_template, current_app
from flask_mail import Message
from sqlalchemy import create_engine
from app import mail


import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from platform import python_version


def send_async_email(app, subject, sender, recipients, text_body, html_body):
    msg = Message(subject, sender=sender, recipients=recipients)
    msg.body = text_body
    msg.html = html_body
    with app.app_context():
        mail.send(msg)


def send_email(subject, sender, recipients, text_body, html_body):
    from main import app
    Thread(target=send_async_email,
           args=(app, subject, sender, recipients, text_body, html_body)).start()


def send_mail_new(project_number, typ, number=0):
    from main import app
    Thread(target=async_mail_new,
           args=(app, project_number, typ, number)).start()


def async_mail_new(app, project_number, type, number):
    from app.models import Expert, User
    with app.app_context():
        engine = create_engine(current_app.config['SQLALCHEMY_DATABASE_URI'])
        if type == 'users':
            users = User.query.filter_by(project_number=project_number).all()
            engine.dispose()
        elif type == 'experts':
            users = Expert.query.filter_by(project_number=project_number).all()
            engine.dispose()
        else:
            return
        for i in range(number):
            users.pop(0)


        for user in users:
            recipients = user.email
            text = render_template('email/send_password.txt',
                                   user=user, password=user.password_hash)
            html = '<html><head></head><body><p>' + \
                   render_template('email/send_password.html',
                                   user=user, password=user.password_hash)\
                   + '</p></body></html>'

            subject = 'NSPT Ваш пароль'
            sender = current_app.config['MAIL_USERNAME']
            msg = MIMEMultipart('alternative')
            msg['Subject'] = subject
            msg['From'] = '<' + sender + '>'
            msg['Reply-To'] = sender
            msg['Return-Path'] = sender
            msg['X-Mailer'] = 'Python/' + (python_version())
            msg['To'] = recipients

            part_text = MIMEText(text, 'plain')
            part_html = MIMEText(html, 'html')

            msg.attach(part_text)
            msg.attach(part_html)

            mail = smtplib.SMTP(current_app.config['MAIL_SERVER'], current_app.config['MAIL_PORT'])
            mail.starttls()
            mail.login(current_app.config['MAIL_USERNAME'], current_app.config['MAIL_PASSWORD'])
            mail.sendmail(sender, recipients, msg.as_string().encode('utf-8'))
            mail.quit()
            time.sleep(10)

