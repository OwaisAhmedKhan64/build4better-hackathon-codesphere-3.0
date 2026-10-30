from typing import Optional, Any
from pydantic import BaseModel, Field

class NoteCreate(BaseModel):
    title: str = Field(..., min_length=1, description="Title of the note or test record")

class NoteResponse(BaseModel):
    id: int
    title: str
    created_at: Optional[str] = None

class SystemStatus(BaseModel):
    status: str
    message: Optional[str] = None
    data: Optional[Any] = None
