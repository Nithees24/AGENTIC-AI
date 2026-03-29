from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware

from llm.llm_client import LLMClient
from agents.general_chat_agent import GeneralChatAgent

app = FastAPI()

# ✅ Enable CORS (frontend can call backend)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # later restrict this
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ✅ Initialize once
llm_client = LLMClient()
general_agent = GeneralChatAgent(llm_client)

# ✅ Request schema (matches your frontend)
class ChatRequest(BaseModel):
    message: str
    mode: str = "Chat Agent"
    messages: list = []

# ✅ API endpoint
@app.post("/api/chat")
def chat(req: ChatRequest):
    try:
        # For now → only general chat
        reply = general_agent.run(req.message)

        return {"reply": reply}

    except Exception as e:
        return {"error": str(e)}