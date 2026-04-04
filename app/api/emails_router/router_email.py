from fastapi import APIRouter, Request
from agents.base.main_agents import send_quick_emails, conversation_email

from app.api.services.read_emails import read_latest_emails
from app.api.services.email_suggesions import emails_suggest_reply
from app.api.services.send_emails import send_email as send_direct_email

router = APIRouter()

# Quick Email by Greeting to Anyone email
@router.post("/send_quick_email")
async def quick_email(request: Request):
    try:
        email_data = await request.json()

        name = email_data.get("name")
        email = email_data.get("send_mail_to")
        
        print(email_data, name, email)

        result = await send_quick_emails(
            f"you are an {name}. send email to {email} using tool. subject set as greeting and in body set the message"
        )

        return {"status": "success", "data": result}
    except Exception as e:
        return {"status": "error", "message": str(e)}

# Sending the email with subject and body by custom prompt
@router.post("/send_email")
async def send_email_sug(request: Request):
    try:
        email_data = await request.json()
        print(email_data)
        email = email_data.get("to")
        subject = email_data.get("subject")
        body = email_data.get("body")

        print(email_data, email)

        # Using the AI agent to send since the current code passes a prompt string
        result = await send_quick_emails(
            f"you are an AI assesstent. send email to {email} using tool." 
            f"subject set as {subject} and in body set the message {body}"
        )

        return {"status": "success", "data": result}
    except Exception as e:
        return {"status": "error", "message": str(e)}
    
# Fetch the emails from inbox
@router.get("/read_emails")
async def read_emails():
    result = await read_latest_emails()
    return result

# Suggest the reply for the email
@router.post("/emails_suggest_reply")
async def suggest_reply_route(request: Request):
    try:
        email_data = await request.json()
        email_content = email_data.get("emailContent")
        print(email_data)
        if not email_content:
             return {"status": "error", "message": "emailContent is required"}
        result = await emails_suggest_reply(email_content)
        
        # Check if the result inherently contains suggestions since sometimes the frontend expects data.suggestions.
        # But wait, next.js dashboard code expects: data = await res.json(); setSuggestions(data.suggestions || [])
        # AND our route wrapper wraps it in {"status": "success", "data": result}. So we should perhaps unpack it correctly:
        # Actually page.tsx returns data.suggestions ? No, page.tsx handles res.json(), which is what router returns.
        return result
    except Exception as e:
        return {"status": "error", "message": str(e)}
