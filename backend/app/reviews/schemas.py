from pydantic import BaseModel
from uuid import UUID
from datetime import datetime

class ReviewCreate(BaseModel):
    reviewer_role: str
    content: str

class ReviewResponse(BaseModel):
    id: UUID
    startup_id: UUID
    user_id: UUID
    content: str
    verified: bool
    created_at: datetime

    class Config:
        from_attributes = True
