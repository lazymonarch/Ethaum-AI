from pydantic import BaseModel, Field
from uuid import UUID
from datetime import datetime

class EnterpriseFeedbackCreate(BaseModel):
    startup_id: str
    rating: int = Field(ge=1, le=5)
    content: str

class EnterpriseFeedbackResponse(BaseModel):
    id: UUID
    startup_id: UUID
    enterprise_id: UUID
    rating: int
    content: str
    verified: bool
    created_at: datetime


    class Config:
        from_attributes = True
