import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from config import EMAIL_USER, EMAIL_APP_PASSWORD

def send_due_reminder(to_email, book_title, due_date):
    subject = f"Library Book Reminder: '{book_title}' Due Soon"
    body = f"""
    Dear Member,

    This is a reminder that the book '{book_title}' is due on {due_date}.
    Please return it to the library on time to avoid fines.

    Thank you,
    Library Management System
    """
    send_email(to_email, subject, body)

def send_overdue_notification(to_email, book_title, days_overdue, fine):
    subject = f"Overdue Book: '{book_title}'"
    body = f"""
    Dear Member,

    The book '{book_title}' is {days_overdue} days overdue.
    Current fine: ${fine}

    Please return the book as soon as possible.

    Thank you,
    Library Management System
    """
    send_email(to_email, subject, body)

def send_email(to_email, subject, body):
    msg = MIMEMultipart()
    msg['From'] = EMAIL_USER
    msg['To'] = to_email
    msg['Subject'] = subject
    msg.attach(MIMEText(body, 'plain'))

    try:
        server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
        server.login(EMAIL_USER, EMAIL_APP_PASSWORD)
        server.sendmail(EMAIL_USER, to_email, msg.as_string())
        server.quit()
        print(f"Email sent to {to_email}")
    except Exception as e:
        print(f"Failed to send email: {e}")