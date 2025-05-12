import uuid
from fastapi import APIRouter
from pydantic import BaseModel, Field
from services.memory import get_history, append_history, get_profile, set_profile
from services.rag import get_answer
from services.logger import log_event
# from services.logger import log_usage, log_qa

router = APIRouter()

class ChatRequest(BaseModel):
    question: str = Field(..., min_length=1, max_length=500)
    session_id: str | None = None

class Citation(BaseModel):
    id: str
    source: str

class ChatResponse(BaseModel):
    answer: str
    citations: list[Citation]
    session_id: str
    cost_usd: float

@router.get("/welcome", response_model=ChatResponse)
async def welcome():
    sid = str(uuid.uuid4())

    welcome = (
      "👋 Welcome to Lens4U! To give you personalized advice, "
      "what type of lenses do you wear? (e.g., daily, monthly, toric)"
    )
    await append_history(sid, "assistant", welcome)
    await set_profile(sid, {})
    return ChatResponse(
      answer=welcome,
      citations=[],
      session_id=sid,
      cost_usd=0.0
    )

@router.post("/chat", response_model=ChatResponse)
async def chat_endpoint(request: ChatRequest):
    sid = request.session_id or str(uuid.uuid4())
    history = await get_history(sid)
    profile = await get_profile(sid)

    if "lens_type" not in profile:
        lens_type = request.question.strip().lower()
        profile["lens_type"] = lens_type
        await set_profile(sid, profile)

        msg = f"Great—you wear {lens_type} lenses. How can I help you today?"
        await append_history(sid, "user", request.question)
        await append_history(sid, "assistant", msg)

        return ChatResponse(
          answer=msg,
          citations=[],
          session_id=sid,
          cost_usd=0.0
        )

    profile = await get_profile(sid)
    lens_type = profile.get("lens_type")
    answer, citations, cost = await get_answer(request.question, sid, history, lens_type)
    await append_history(sid, "user", request.question)
    await append_history(sid, "assistant", answer)

    log_event("OPENAI_USAGE", {
      "session_id": sid,
      "tokens":   cost["tokens"],
      "cost_usd": cost["usd"]
    })
    # log_usage(sid, cost["tokens"], cost["usd"])

    return ChatResponse(
      answer=answer,
      citations=[Citation(**c) for c in citations],
      session_id=sid,
      cost_usd=cost["usd"]
    )