from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app.services.dialogue_service import DialogueService
from app.services.session_service import SessionService
from app.api import deps
from app.core.generator.llm_client import LLMClient
from app.api.v1.models.dialogue import (
    ChatRequest, ChatResponse, SessionCreateRequest, SessionResponse,
    MessageResponse
)

router = APIRouter()

@router.get("/test")
async def test_dialogue():
    return {"message": "Dialogue endpoint is active"}




def get_dialogue_service(db: Session = Depends(deps.get_db_session)) -> DialogueService:
    return DialogueService(db , LLMClient())

def get_session_service(db: Session = Depends(deps.get_db_session)) -> SessionService:
    return SessionService(db)

@router.post("/session/start", response_model=SessionResponse)
def start_session(
    req: SessionCreateRequest,
    session_svc: SessionService = Depends(get_session_service)
):
    """创建新会话，返回 session_id"""
    session_id = session_svc.create_session(user_name=req.user_name)
    return SessionResponse(session_id=session_id, message="会话已创建")


@router.post("/message", response_model=ChatResponse)
def send_message(
    req: ChatRequest,
    session_id: str = Depends(deps.get_session_id),
    dialogue_svc: DialogueService = Depends(get_dialogue_service),
    db: Session = Depends(deps.get_db_session)
):
    """发送文字消息，获取智能体回复"""
    # 若会话不存在，服务层会自动创建或抛出异常
    try:
        reply = dialogue_svc.process_message(session_id, req.text)
        # 同时获取当前意图状态（可选）
        intent_status = dialogue_svc.get_intent_status(session_id)
        return ChatResponse(
            reply=reply,
            intent_status=intent_status,
            session_id=session_id
        )
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))

@router.get("/history", response_model=List[MessageResponse])
def get_history(
    session_id: str = Depends(deps.get_session_id),
    dialogue_svc: DialogueService = Depends(get_dialogue_service)
):
    """获取会话的对话历史"""
    messages = dialogue_svc.get_history(session_id)
    return [MessageResponse(role=m.role, content=m.content, timestamp=m.created_at) for m in messages]

