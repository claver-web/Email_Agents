from fastapi import APIRouter, Request
from agents.base.main_agents import send_quick_emails, conversation_email

from app.api.services.read_emails import read_latest_emails
from app.api.services.email_suggesions import emails_suggest_reply
from app.api.services.send_emails import send_email as send_direct_email
from app.api.services.ai_generation import generate_email_content

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
        print(email_data, email)
        
        # Extract optional authentication if provided by the Next.js bridge
        auth_data = email_data.get("auth", {})
        sender_email = auth_data.get("user")
        sender_password = auth_data.get("pass")

        # Use direct SMTP sending for reliability
        result = await send_direct_email(
            email, 
            subject, 
            body, 
            sender_email=sender_email, 
            sender_password=sender_password
        )

        return result
    except Exception as e:
        return {"status": "error", "message": str(e)}
    
# Fetch the emails from inbox
@router.get("/read_emails")
async def read_emails():
    result = await read_latest_emails()
    return result

# Suggest the reply for the email
@router.api_route("/emails_suggest_reply", methods=["GET", "POST"])
async def suggest_reply_route(request: Request):
    if request.method == "GET":
        return {"status": "success", "message": "Email suggestion endpoint is active and waiting for POST data."}
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

# Generate AI campaign content
@router.post("/generate_campaign")
async def generate_campaign_route(request: Request):
    try:
        data = await request.json()
        prompt = data.get("prompt")
        tone = data.get("tone", "professional")
        
        if not prompt:
            return {"status": "error", "message": "Prompt is required"}
            
        result = await generate_email_content(prompt, tone)
        return result
    except Exception as e:
        return {"status": "error", "message": str(e)}

