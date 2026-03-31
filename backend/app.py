from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware

from backend.llm.llm_client import LLMClient
from backend.agents.general_chat_agent import GeneralChatAgent
from backend.agents.deep_research_agent import DeepResearchAgent
from backend.pipeline.planner import Planner

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
deep_agent = DeepResearchAgent(llm_client)
planner = Planner(llm_client)

# ✅ Request schema (matches your frontend)
class ChatRequest(BaseModel):
    message: str
    mode: str = "Chat Agent"
    messages: list = []

# ✅ API endpoint
@app.post("/api/chat")
def chat(req: ChatRequest):
    try:
        # 🔥 1. UI override (highest priority)
        if req.mode == "Deep Research":
            reply = deep_agent.run(req.message)
            return {"reply": reply}

        # 🔥 2. Smart auto-routing using planner
        plan = planner.plan(req.message)
        mode = plan.get("mode")

        if mode == "deep_research":
            reply = deep_agent.run(req.message)
        else:
            reply = general_agent.run(req.message)

        return {"reply": reply}

    except Exception as e:
        return {"error": str(e)}
