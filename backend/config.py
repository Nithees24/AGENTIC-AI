import os

PRODUCTION = os.getenv("PRODUCTION", "False").lower() == "true"

LLM_MODEL = "gemini-3.1-flash-lite-preview"
TEMPERATURE = 0.2