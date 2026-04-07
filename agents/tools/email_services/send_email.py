from app.core.config import settings
import smtplib
import os
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


def send_email(
    to_email: str,
    subject: str,
    body: str,
    sender_email: str = settings.SENDER_EMAIL,
    app_password: str = settings.EMAIL_PASSWORD
):
    """
    Send an email via Gmail SMTP.

    Args:
        to_email (str): receiver email
        subject (str): email subject
        body (str): email body text
        sender_email (str): sender gmail
        app_password (str): gmail app password
    """

    try:
        msg = MIMEMultipart()
        msg["From"] = sender_email
        msg["To"] = to_email
        msg["Subject"] = subject

        msg.attach(MIMEText(body, "plain"))

        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()
        server.login(sender_email, app_password)

        server.send_message(msg)
        server.quit()

        return "Email sent successfully"

    except Exception as e:
        return f"Email sending failed: {str(e)}"