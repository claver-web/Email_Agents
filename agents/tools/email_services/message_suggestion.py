import os
from agno.agent import Agent
from agno.models.ollama import Ollama
from agno.db.json import JsonDb

# ---------- MODEL ----------
model = Ollama(
    id="qwen2.5:3b-instruct",
    host="http://localhost:11434"
)

db = JsonDb(db_path="../memory/suggestion.json")

# ---------- AGENT ----------
agent = Agent(model=model, stream=False, db=db, add_history_to_context=True)

# ---------- FUNCTION ----------
def suggest_email_reply(email_text: str):
    prompt = f"""
You are Kartik Mehra replying to emails personally.

Your task:
Generate 3 different reply options based on the email context.

Understand the intent first, then respond naturally.

Tone styles:
1. Professional (polite, structured)
2. Friendly (warm, conversational)
3. Direct (short, to the point)

Rules:
- Sound like a real human (NOT AI)
- Avoid generic lines like "Hope you are doing well"
- Keep replies concise (3–6 lines max)
- Make each option meaningfully different (not reworded copies)
- If appropriate, include a simple follow-up question
- Keep language simple and natural (like a real person typing)
- DO NOT change format. Always use exactly "Option 1:", "Option 2:", "Option 3:"

Output STRICTLY in this format:

Option 1:
Subject: <short subject>
Body:
<reply>

--

Option 2:
Subject: <short subject>
Body:
<reply>

--

Option 3:
Subject: <short subject>
Body:
<reply>

--

Signature (same for all):
Kartik Mehra
📞 9898989898

Email:
{email_text}
"""

    response = agent.run(prompt)
    return str(response.content if hasattr(response, "content") else response)


# ---------- FUNCTION Without Suggestion ----------
def email_reply(email_text: str):
    prompt = f"""
    You are Kartik Mehra replying to an email personally.

    STEP 1 — Understand:
    - Identify the sender’s intent (question, request, complaint, proposal, etc.)
    - Extract key details that must be addressed

    STEP 2 — Respond:
    Write ONE clear and natural email reply.

    TONE:
    - Choose the most appropriate tone automatically:
    • Professional → for formal/business emails  
    • Friendly → for casual or known contacts  
    • Direct → for quick or transactional replies  

    WRITING RULES:
    - Sound like a real human (not AI)
    - Do NOT use phrases like "Hope you are doing well" or "As per your email"
    - Keep it concise (3–6 lines max)
    - Use simple, natural language
    - Address the main intent clearly
    - If useful, include ONE natural follow-up question
    - Avoid repetition or unnecessary fluff

    OUTPUT FORMAT (STRICT):

    Subject: <clear and relevant subject>
    Body:
    <email reply>

    Signature:
    Kartik Mehra
    📞 9898989898

    EMAIL TO REPLY:
    {email_text}
"""

    response = agent.run(prompt)
    return str(response.content if hasattr(response, "content") else response)
