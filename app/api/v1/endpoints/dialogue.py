import json

from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import StreamingResponse
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

@router.post("/chat", response_model=MessageResponse)
async def chat(
    req: ChatRequest,
    session_id: str = Depends(deps.get_session_id),
    dialogue_svc: DialogueService = Depends(get_dialogue_service),
    db: Session = Depends(deps.get_db_session)
):
    """
       纯粹的对话流式接口
       """

    # 定义一个异步生成器来处理 SSE 格式
    async def stream_generator():
        # chat_service.chat_stream 是一个异步生成器
        async for chunk in dialogue_svc.chat_stream(session_id, req.text):
            # 格式化为 SSE 格式
            # 注意：这里假设 chunk 是字符串
            yield f"data: {json.dumps({'content': chunk}, ensure_ascii=False)}\n\n"

        # 发送结束信号
        yield f"data: {json.dumps({'content': '', 'done': True}, ensure_ascii=False)}\n\n"

    # 返回流式响应
    # 直接传入异步生成器
    return StreamingResponse(stream_generator(), media_type="text/plain")

@router.post("/intent_message", response_model=ChatResponse)
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

