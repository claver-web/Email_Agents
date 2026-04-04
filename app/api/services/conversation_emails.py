import os
import imaplib
import smtplib
import email
import time

from dotenv import load_dotenv
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.header import decode_header

from agents.tools.email_services.message_suggestion import suggest_email_reply, email_reply
# from tools.wait_and_get_return_from_user import wait_and_get_return_from_user

load_dotenv()


def email_conversation_bot(
    partner_email: str,
    first_message: str,
    subject: str,
    check_interval: int = 15,
):
    """
    Start conversation with specific email and auto-reply to replies.
    """

    sender_email = os.getenv("SENDER_EMAIL")
    app_password = os.getenv("EMAIL_APP_PASS")

    if not sender_email or not app_password:
        return "Email credentials not configured"

    print(f"🚀 Starting conversation with {partner_email}")

    # ---------- SEND FIRST MESSAGE ----------
    
    msg = MIMEMultipart()
    msg["From"] = sender_email
    msg["To"] = partner_email
    msg["Subject"] = subject

    msg.attach(MIMEText(first_message, "plain"))

    smtp = smtplib.SMTP("smtp.gmail.com", 587)
    smtp.starttls()
    smtp.login(sender_email, app_password)
    smtp.send_message(msg)
    smtp.quit()

    print("✅ First message sent")

    last_seen_uid = None

    while True:
        try:
            imap = imaplib.IMAP4_SSL("imap.gmail.com")
            imap.login(sender_email, app_password)
            imap.select("inbox")

            status, messages = imap.search(
                None,
                f'(UNSEEN FROM "{partner_email}")'
            )

            mail_ids = messages[0].split()

            if mail_ids:
                latest = mail_ids[-1]

                if latest != last_seen_uid:

                    res, msg = imap.fetch(latest, "(RFC822)")
                    raw = msg[0][1]
                    msg_obj = email.message_from_bytes(raw)

                    subject = msg_obj.get("Subject", "")

                    sub, enc = decode_header(subject)[0]
                    if isinstance(sub, bytes):
                        subject = sub.decode(
                            enc if enc else "utf-8",
                            errors="ignore"
                        )

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

                    print("📩 Reply:", subject)

                    # reply_body = suggest_email_reply(body_text)
                    reply_body = email_reply(body_text)
                    # selected_reply = wait_and_get_return_from_user(reply_body)
                    subject_line, body = parse_selected_reply(reply_body)

                    reply = MIMEMultipart()
                    reply["From"] = sender_email
                    reply["To"] = partner_email
                    reply["Subject"] = subject_line if subject_line else "Re: " + subject
                    reply.attach(MIMEText(body, "plain"))
                    
                    smtp = smtplib.SMTP("smtp.gmail.com", 587)
                    smtp.starttls()
                    smtp.login(sender_email, app_password)
                    smtp.send_message(reply)
                    smtp.quit()

                    print("✅ Reply sent")

                    imap.store(latest, "+FLAGS", "\\Seen")

                    last_seen_uid = latest

            imap.logout()

        except Exception as e:
            print("❌ Error:", e)

        time.sleep(check_interval)

def parse_selected_reply(text):
    subject = ""
    body = ""

    if "Subject:" in text:
        subject = text.split("Subject:")[1].split("\n")[0].strip()

    if "Body:" in text:
        body = text.split("Body:")[1].split("--")[0].strip()

    return subject, body