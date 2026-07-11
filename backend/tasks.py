from celery_worker import celery_app
from models import User , Student , Company , Application , PlacementDrive
from auth import admin_required , company_required , student_required
from datetime import datetime

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import smtplib
from flask import render_template


#==============email configuration=====================

SMTP_HOST = 'localhost'
SMTP_PORT = 1025
SENDER_EMAIL = 'PlaceMeFirst@gmail.com'
SENDER_PASSWORD = ''




@celery_app.task
def send_registration_email(user_email, user_name):
    # Email message setup
    msg = MIMEMultipart()
    msg['From'] = SENDER_EMAIL
    msg['To'] = user_email
    msg['Subject'] = "Welcome to PlaceMeFirst!"

    # Template render karein
    body = render_template('welcome.html', name=user_name , user_id = user_id)
    msg.attach(MIMEText(body, 'html'))

    # Send email
    try:
        server = smtplib.SMTP(SMTP_HOST, SMTP_PORT)
        server.send_message(msg)
        server.quit()
        return f"Email successfully sent to {user_email}"
    except Exception as e:
        return f"Error sending email: {str(e)}"

