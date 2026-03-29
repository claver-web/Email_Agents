from agno.agent import Agent
from agno.models.ollama import Ollama
from agents.tools.email_services.send_email import send_email
from agents.tools.email_services.read_emails import read_latest_emails

import json

model = Ollama(
    id="qwen2.5:3b-instruct",
    host="http://localhost:11434"
)

agent = Agent(
    model=model,
    tools=[send_email, read_latest_emails]
)

async def email_msg(message: str):
    result = agent.run(message)
    return result.content

async def send_email_msg():
    result = agent.run("send email to kartikmehra173@gmail.com with greeting and add subject of greeting.")
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