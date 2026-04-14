from agents.base.main_agents import agent
import json

async def generate_email_content(prompt: str, tone: str):
    full_prompt = f"""
    You are an expert AI email copywriter. 
    Generate a compelling email based on the following instructions:
    
    Topic/Prompt: {prompt}
    Tone: {tone}
    
    The email must include:
    1. A catchy Subject Line.
    2. A professional yet engaging Body.
    
    Use placeholders like {{name}} and {{email}} where appropriate.
    
    Return EXACTLY AND ONLY valid JSON format.
    The JSON should have two keys: "subject" and "body".
    
    Do not add any markdown, code blocks, or extra text outside the JSON.
    """
    
    try:
        result = agent.run(full_prompt)
        raw = result.content
        
        try:
            return json.loads(raw)
        except json.JSONDecodeError:
            # Cleanup common AI formatting artifacts
            cleaned = raw.replace('```json', '').replace('```', '').strip()
            return json.loads(cleaned)
            
    except Exception as e:
        print(f"AI Generation Error: {e}")
        return {
            "subject": f"Update: {prompt[:30]}...",
            "body": f"I was unable to generate a full response, but here is a draft based on: {prompt}\n\nTone: {tone}"
        }
