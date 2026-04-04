import smtplib
import asyncio
from email.message import EmailMessage
from app.core.config import settings

def _send_email_sync(to: str, subject: str, body: str):
    email_sender = settings.SENDER_EMAIL
    email_password = settings.EMAIL_PASSWORD

    msg = EmailMessage()
    msg['Subject'] = subject
    msg['From'] = email_sender
    msg['To'] = to
    msg.set_content(body)

    try:
        # Note: if using Gmail, check if you need to use an App Password
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
            smtp.login(email_sender, email_password)
            smtp.send_message(msg)
            return {"status": "success", "message": "Email sent successfully"}
    except Exception as e:
        print(f"Error sending email: {e}")
        return {"status": "error", "message": str(e)}

async def send_email(to: str, subject: str, body: str):
    """
    Sends an email asynchronously to avoid blocking the main thread.
    """
    return await asyncio.to_thread(_send_email_sync, to, subject, body)