import json
import re
import uuid
from agents.base.main_agents import agent

async def emails_suggest_reply(email_content: str):
    prompt = f"""
    You are an AI email assistant. 
    Analyze the following email and generate exactly 3 smart reply suggestions.
    The suggestions should cover different tones (e.g., Professional, Casual, Polite Decline, or Helpful).
    
    Email Content:
    {email_content}
    
    Return EXACTLY AND ONLY valid JSON format.
    The JSON should be an object with a "suggestions" key containing an array of 3 suggestion objects.
    Each suggestion object must have these exactly 3 keys:
    "id": a unique string ID (e.g. "sug-1")
    "label": a short 1-3 word tone label (e.g. "Professional", "Polite Decline")
    "text": the full suggested reply text body
    
    Format example:
    {{
      "suggestions": [
        {{
          "id": "1",
          "label": "Professional",
          "text": "Thank you for reaching out..."
        }}
      ]
    }}
    
    Do not add any markdown, code blocks, or extra text outside the JSON.
    """
    try:
        # Agent calls are sometimes synchronous, so we run it directly
        result = agent.run(prompt)
        raw = result.content
        
        try:
            return json.loads(raw)
        except json.JSONDecodeError:
            # Fallback cleanup attempts
            cleaned = raw.replace('```json', '').replace('```', '').strip()
            return json.loads(cleaned)
            
    except Exception as e:
        return {"status": "error", "message": "Failed to generate suggestions", "details": str(e), "suggestions": []}
    