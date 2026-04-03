from app.core.config import settings
from agno.agent import Agent
from agno.models.google import Gemini
from tools.send_email import send_email

model = Gemini(
    id="gemini-3-flash-preview",
    temperature=0.7,
    api_key=settings.GEMINI_API_KEY
)

# Create agent
agent = Agent(
    model=model,
    instructions="You are a helpful AI assistant. WHo read and send email to someone.",
    stream=True,
    tools= [send_email]
)