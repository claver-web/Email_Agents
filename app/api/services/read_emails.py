from app.core.config import settings
import imaplib
import email
from email.header import decode_header
import asyncio

def _read_latest_emails_sync(limit: int = 15):
    """
    Synchronous helper to read latest emails from Gmail inbox.
    """
    EMAIL = settings.SENDER_EMAIL
    PASS = settings.EMAIL_PASSWORD

    results = []

    try:
        imap = imaplib.IMAP4_SSL("imap.gmail.com", timeout=30)  # Add timeout
        imap.login(EMAIL, PASS)
        imap.select("inbox")

        status, messages = imap.search(None, "ALL")

        if status != "OK":
            return results

        mail_ids = messages[0].split()
        latest = mail_ids[-limit:]

        for i in reversed(latest):
            res, msg = imap.fetch(i, "(RFC822)")
            for response in msg:
                if isinstance(response, tuple):
                    msg_obj = email.message_from_bytes(response[1])
                    subject, encoding = decode_header(msg_obj.get("Subject"))[0]

                    if isinstance(subject, bytes):
                        subject = subject.decode(encoding if encoding else "utf-8", errors="ignore")

                    from_ = msg_obj.get("From")
                    body_text = ""

                    if msg_obj.is_multipart():
                        for part in msg_obj.walk():
                            if part.get_content_type() == "text/plain":
                                payload = part.get_payload(decode=True)
                                if payload:
                                    body_text = payload.decode(errors="ignore")
                                break
                    else:
                        payload = msg_obj.get_payload(decode=True)
                        if payload:
                            body_text = payload.decode(errors="ignore")

                    results.append({
                        "from": from_,
                        "subject": subject,
                        "body": body_text  # Full body
                    })
        
        imap.close()
        imap.logout()
        
    except imaplib.IMAP4.error as e:
        print(f"IMAP Error: {e}")
        return []
    except Exception as e:
        print(f"General Error: {e}")
        return []

    return results

async def read_latest_emails(limit: int = 15):
    """
    Reads latest emails from Gmail inbox asynchronously (non-blocking).
    """
    try:
        return await asyncio.wait_for(
            asyncio.to_thread(_read_latest_emails_sync, limit),
            timeout=30.0  # 30 second timeout
        )
    except asyncio.TimeoutError:
        print("Email fetching timed out")
        return []