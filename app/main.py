from fastapi import FastAPI
from app.api.emails_router import email_send
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

allow_host = ["http://localhost:3000", "*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=allow_host,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(email_send.router, prefix="/api")