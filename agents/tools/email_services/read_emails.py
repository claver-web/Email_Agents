from app.core.config import settings
import imaplib
import email
from email.header import decode_header


def read_latest_emails(limit: int = 5):
    """
    Reads latest emails from Gmail inbox.

    Args:
        limit (int): number of latest emails to fetch

    Returns:
        list[dict]: structured email data
    """

    EMAIL = settings.SENDER_EMAIL
    PASS = settings.EMAIL_PASSWORD

    results = []

    imap = imaplib.IMAP4_SSL("imap.gmail.com")
    imap.login(EMAIL, PASS)

    imap.select("inbox")

    status, messages = imap.search(None, "ALL")

    if status != "OK":
        imap.logout()
        return results

    mail_ids = messages[0].split()
    latest = mail_ids[-limit:]

    for i in reversed(latest):

        res, msg = imap.fetch(i, "(RFC822)")

        for response in msg:
            if isinstance(response, tuple):

                msg_obj = email.message_from_bytes(response[1])

                subject, encoding = decode_header(
                    msg_obj.get("Subject")
                )[0]

                if isinstance(subject, bytes):
                    subject = subject.decode(
                        encoding if encoding else "utf-8",
                        errors="ignore"
                    )

                from_ = msg_obj.get("From")

                body_text = ""

                if msg_obj.is_multipart():
                    for part in msg_obj.walk():
                        if part.get_content_type() == "text/plain":
                            body_text = part.get_payload(
                                decode=True
                            ).decode(errors="ignore")
                            break
                else:
                    body_text = msg_obj.get_payload(
                        decode=True
                    ).decode(errors="ignore")

                email_data = {
                    "from": from_,
                    "subject": subject,
                    "body": body_text[:300]
                }

                results.append(email_data)

    imap.logout()

    return results