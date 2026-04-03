from app.core.config import settings
from agno.models.ollama import Ollama
from agno.models.google import Gemini

Gemini_model = Gemini(
    id="gemini-3-flash-preview",
    temperature=0.7,
    api_key=settings.GEMINI_API_KEY
)

Ollama_model = Ollama(
    id="qwen2.5:3b-instruct",
    host="http://localhost:11434"
)