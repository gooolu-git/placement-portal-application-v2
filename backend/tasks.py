from celery_worker import celery_app
from models import User , Student , Company , Application , PlacementDrive
from auth import admin_required , company_required , student_required
from datetime import datetime,timedelta

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import smtplib
from flask import render_template
from sqlalchemy import func
import csv
import io
from email.mime.application import MIMEApplication

#==============email configuration=====================

SMTP_HOST = 'localhost'
SMTP_PORT = 1025
SENDER_EMAIL = 'PlaceMeFirst@gmail.com'
SENDER_PASSWORD = ''

@celery_app.task
def send_email(to_add, subject, name, user_id):
    """
    Celery task to send personalized reminder emails to students 
    who haven't applied to an upcoming placement drive yet.
    """
    # Email message setup
    msg = MIMEMultipart()
    msg['From'] = SENDER_EMAIL
    msg['To'] = to_add
    msg['Subject'] = subject


    try:
        body = render_template('remainder.html', name=name, user_id=user_id)
        msg.attach(MIMEText(body, 'html'))
    except Exception as e:
        return f"Template rendering error: {str(e)}"


    try:
        server = smtplib.SMTP(SMTP_HOST, SMTP_PORT)
        server.send_message(msg)
        server.quit()
        return f"Reminder email successfully sent to {to_add}"
    except Exception as e:
        return f"Error sending email to {to_add}: {str(e)}"


@celery_app.task
def send_registration_email(user_email, user_name,user_id):

    msg = MIMEMultipart()
    msg['From'] = SENDER_EMAIL
    msg['To'] = user_email
    msg['Subject'] = "Welcome to PlaceMeFirst!"


    body = render_template('welcome.html', name=user_name , user_id = user_id)
    msg.attach(MIMEText(body, 'html'))


    try:
        server = smtplib.SMTP(SMTP_HOST, SMTP_PORT)
        server.send_message(msg)
        server.quit()
        return f"Email successfully sent to {user_email}"
    except Exception as e:
        return f"Error sending email: {str(e)}"

@celery_app.task
def send_daily_remainder():
    now = datetime.now()
    deadline_coming = now + timedelta(days=30)
    upcoming_placement_drives = PlacementDrive.query.filter(PlacementDrive.deadline>now,
    PlacementDrive.deadline<=deadline_coming).all()
    sent_count = 0
    for drive in upcoming_placement_drives:
        applied_student_ids = [app.student_id for app in drive.applications]
        eligible_stundet= Student.query.filter(
            Student.id.notin_(applied_student_ids)
        ).all()
        for student in eligible_stundet:
            send_email.delay(
                    to_add=student.user.email,
                    subject=f"Urgent: {drive.job_title} Application Deadline Approaching",
                    name=student.user.name,
                    user_id=student.user.id
                )
            sent_count += 1       
    return f"Daily reminder task completed. Sent {sent_count} reminders."



@celery_app.task
def send_monthly_report():
    """
    Generates a monthly placement activity report for the past month
    and emails it directly to the platform administrator.
    """
    now = datetime.now()
    
    # Calculate the first and last day of the PREVIOUS month
    first_day_this_month = now.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
    last_day_prev_month = first_day_this_month - timedelta(days=1)
    first_day_prev_month = last_day_prev_month.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
    
    month_name = first_day_prev_month.strftime('%B %Y')

    # --- 1. Fetch Metrics ---
    drives_count = PlacementDrive.query.filter(
        PlacementDrive.deadline >= first_day_prev_month,
        PlacementDrive.deadline <= last_day_prev_month
    ).count()

    total_applied = Application.query.filter(
        Application.applied_on >= first_day_prev_month,
        Application.applied_on <= last_day_prev_month
    ).count()

    total_selected = Application.query.filter(
        Application.applied_on >= first_day_prev_month,
        Application.applied_on <= last_day_prev_month,
        Application.status == 'Selected' 
    ).count()

    # --- 2. Target the Single Admin ---
    # Using .first() because there is only one system admin
    admin = User.query.filter(User.role == 'admin', User.is_approved == True).first()
    
    if not admin:
        return "Report generation canceled: Admin account not found or not approved."

    # --- 3. Build & Dispatch Email ---
    msg = MIMEMultipart()
    msg['From'] = SENDER_EMAIL
    msg['To'] = admin.email
    msg['Subject'] = f"PlaceMeFirst: Monthly Activity Report - {month_name}"

    try:
        body = render_template(
            'monthly_report.html',
            admin_name=admin.name,
            month_name=month_name,
            drives_count=drives_count,
            total_applied=total_applied,
            total_selected=total_selected,
            generated_on=now.strftime('%Y-%m-%d %H:%M')
        )
        msg.attach(MIMEText(body, 'html'))
    except Exception as e:
        return f"Template rendering error: {str(e)}"

    try:
        server = smtplib.SMTP(SMTP_HOST, SMTP_PORT)
        server.send_message(msg)
        server.quit()
        return f"Monthly report successfully generated and sent to Admin ({admin.email})."
    except Exception as e:
        return f"Failed sending report to admin email {admin.email}: {str(e)}"

@celery_app.task
def ExportApplications(student_id, student_email, student_name):
    apps = Application.query.filter_by(student_id=student_id).all()
    
    # 2. Write CSV to memory
    output = io.StringIO()
    writer = csv.writer(output)
    writer.writerow(["Student ID", "Company Name", "Drive Title", "Application Status", "Date Applied"])
    
    for app_entry in apps:
        # Added safety checks in case relationships are None
        company_name = app_entry.target_drive.company_owner.company_name if app_entry.target_drive and app_entry.target_drive.company_owner else "N/A"
        drive_title = app_entry.target_drive.job_title if app_entry.target_drive else "N/A"
        date_applied = app_entry.applied_on.strftime('%Y-%m-%d') if app_entry.applied_on else "N/A"

        writer.writerow([
            app_entry.student_id,
            company_name,
            drive_title,
            app_entry.status,
            date_applied
        ])
        
    csv_data = output.getvalue()
    
    # 3. Prepare Email
    msg = MIMEMultipart()
    msg['From'] = SENDER_EMAIL
    msg['To'] = student_email
    msg['Subject'] = "Your Placement Application History - PlaceMeFirst"
    
    # Professional HTML Body
    email_body = f"""
    <html>
        <body>
            <h2 style="color: #2c3e50;">PlaceMeFirst</h2>
            <p>Hello <b>{student_name}</b>,</p>
            <p>As requested, please find your complete placement application history attached to this email as a CSV file.</p>
            <p>We hope this summary helps you keep track of your career progress.</p>
            <br>
            <p>Best regards,<br>
            <b>The PlaceMeFirst Team</b></p>
            <hr style="border: 0; border-top: 1px solid #eee;">
            <p style="font-size: 12px; color: #7f8c8d;">This is an automated report. Please do not reply to this email.</p>
        </body>
    </html>
    """
    msg.attach(MIMEText(email_body, 'html'))
    
    # 4. Attach CSV
    part = MIMEApplication(csv_data.encode('utf-8'), Name="application_history.csv")
    part['Content-Disposition'] = 'attachment; filename="application_history.csv"'
    msg.attach(part)
    
    # 5. Send
    try:
        server = smtplib.SMTP(SMTP_HOST, SMTP_PORT)
        server.send_message(msg)
        server.quit()
        return f"Export sent to {student_email}"
    except Exception as e:
        return f"Error sending export email: {str(e)}"