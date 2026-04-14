import smtplib
import asyncio
from email.message import EmailMessage
from app.core.config import settings

def _send_email_sync(to: str, subject: str, body: str, sender_email: str = None, sender_password: str = None):
    print(f"[Email Service] Attempting to send email to {to}")
    
    # Use provided credentials if available, otherwise fall back to defaults
    email_sender = sender_email or settings.SENDER_EMAIL
    email_password = sender_password or settings.EMAIL_PASSWORD

    msg = EmailMessage()
    # ... (skipping some logic for brevity unless needed)
    msg['Subject'] = subject
    msg['From'] = email_sender
    msg['To'] = to
    
    # Check if body contains HTML tags to decide subtype
    if "<" in body and ">" in body:
        msg.set_content("This is an HTML email. Please use a compatible reader.")
        msg.add_alternative(body, subtype='html')
    else:
        msg.set_content(body)

    try:
        # Note: if using Gmail, check if you need to use an App Password
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
            smtp.login(email_sender, email_password)
            smtp.send_message(msg)
            return {"status": "success", "message": f"Email sent successfully from {email_sender}"}
    except Exception as e:
        print(f"Error sending email: {e}")
        return {"status": "error", "message": str(e)}

async def send_email(to: str, subject: str, body: str, sender_email: str = None, sender_password: str = None):
    """
    Sends an email asynchronously to avoid blocking the main thread.
    """
    return await asyncio.to_thread(_send_email_sync, to, subject, body, sender_email, sender_password)