from fastapi import APIRouter, Request
from agents.base.main_agents import email_msg, send_emails, conversation_email
from app.api.services.read_emails import read_latest_emails

router = APIRouter()

@router.get("/chat")
async def chat():
    result = await email_msg("hi")
    return {"message": result}

@router.get("/send_email")
async def send_email():
    try:
        # email_data = await request.json()
        to_email = "kartikmehra173@gmail.com" #email_data["send_mail_to"]
        # name = email_data.get("name")

        result = await send_emails(to_email)

        return {"status": "success", "data": result}
    except Exception as e:
        return {"status": "error", "message": str(e)}
    

@router.get("/read_emails")
async def read_emails():
    result = await read_latest_emails()
    return result



@router.get("/email_reply")
async def email_reply():
    result = await conversation_email()
    return result
