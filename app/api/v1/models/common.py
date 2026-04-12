from pydantic import BaseModel
from typing import Optional, Dict, Any

class FileUploadResponse(BaseModel):
    file_id: str
    file_name: str
    message: str

class NoteUpdateResponse(BaseModel):
    message: str

class ParsedResultResponse(BaseModel):
    file_id: str
    parsed_status: str  # pending, processing, completed, failed
    summary: Optional[str] = None
    details: Optional[Dict[str, Any]] = None