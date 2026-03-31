from agno.agent import Agent
from agno.models.google import Gemini
from tools.send_email import send_email

model = Gemini(
    id="gemini-3-flash-preview",
    temperature=0.7,
    api_key="AIzaSyDE_HMtsya4KrMk4pFCS0IqTmerCR9GSaA"
)

# Create agent
agent = Agent(
    model=model,
    instructions="You are a helpful AI assistant.",
    stream=True,
    tools= [send_email]
)

# Run agent
response = agent.print_response("you are an kartik. send email to kartikmehra173@gmail.com using tool. subject set as greeting and in body set the message")

print(response)