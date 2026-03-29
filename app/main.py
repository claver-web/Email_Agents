from fastapi import FastAPI
from app.api.emails_router import email_send

app = FastAPI()

app.include_router(email_send.router, prefix="/api")