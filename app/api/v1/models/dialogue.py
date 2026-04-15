from pydantic import BaseModel
from typing import Optional, List, Dict, Any
from datetime import datetime

class SessionCreateRequest(BaseModel):
    user_name: Optional[str] = None

class SessionResponse(BaseModel):
    session_id: str
    message: str

class AllSessionResponse(BaseModel):
    session_id: str
    content: str

class ChatRequest(BaseModel):
    text: str

class ChatResponse(BaseModel):
    reply: str
    intent_status: Optional[Dict[str, Any]] = None
    session_id: str

class MessageResponse(BaseModel):
    role: str   # user / assistant
    content: str
    timestamp: datetime