from fastapi import APIRouter
from agents.base.main_agents import email_msg, send_email_msg, read_email, conversation_email

router = APIRouter()

@router.get("/chat")
async def chat():
    result = await email_msg("hi")
    return {"message": result}

@router.post("/send_email")
async def send_email(email_data: dict):
    result = await send_email_msg(email_data)
    return {"message": result}

@router.get("/read_emails")
async def read_emails():
    result = await read_email()
    return result

@router.get("/email_reply")
async def email_reply():
    result = await conversation_email()
    return result
