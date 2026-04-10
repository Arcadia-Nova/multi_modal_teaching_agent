from fastapi import APIRouter, Depends
from app.services.dialogue_service import DialogueService
from app.api import deps
from app.core.generator import llm_client

router = APIRouter()

@router.get("/test")
async def test_dialogue():
    return {"message": "Dialogue endpoint is active"}



dialogue_service = DialogueService(llm_client)  # 需传入

@router.post("/chat")
async def chat(
    request: dict,
    session_id: str = Depends(deps.get_session_id)
):
    user_message = request.get("message")
    reply = dialogue_service.process_message(session_id, user_message)
    return {"reply": reply, "session_id": session_id}