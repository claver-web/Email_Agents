from agno.agent import Agent

from agents.main_agent import Gemini_model
from agents.tools.email_services.send_email import send_email as send_email_tool
from agents.tools.email_services.read_emails import read_latest_emails

import json
import re

agent = Agent(
    model=Gemini_model,
    tools=[send_email_tool, read_latest_emails]
)

async def email_msg(message: str):
    result = agent.run(message)
    return result.content

#Send single Quick Email to anyone Greeting message.
async def send_quick_emails(prompt: str):
    result = agent.run(prompt)
    return result.content

#Reading the Latest 5 emails and return in JSON format.
async def read_email():
    prompt = """
        Read the latest 5 emails.

        For each email:
        - extract sender email (only the email, not name)
        - extract subject (single line, no line breaks)
        - summarize in exactly 3 to 4 short lines

        STRICT RULES:
        - No newline characters inside subject
        - No angle brackets in output
        - No extra text

        Return ONLY valid JSON:
        {
            "emails": [
                {
                    "from": "email@example.com",
                    "subject": "string",
                    "summary": "line1\\nline2\\nline3"
                }
            ]
        }
    """

    result = agent.run(prompt)
    raw = result.content

    try:
        return json.loads(raw)
    except json.JSONDecodeError:
        # attempt cleanup
        cleaned = raw

        # fix escaped HTML
        cleaned = cleaned.replace("\\u003C", "<").replace("\\u003E", ">")

        # remove problematic newlines inside strings
        cleaned = re.sub(r'\\n', ' ', cleaned)

        try:
            return json.loads(cleaned)
        except Exception:
            return {"error": "Still invalid JSON", "raw": raw}

async def conversation_email():
    result = agent.run("send emailto partner kartikmehra173@gmail.com with greeting, andadd subject of greeting. and start the professional conversation like human. read the email context. then baises of the context replt back.")
    return result.content