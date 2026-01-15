from pydantic import BaseModel
from uuid import UUID
from datetime import datetime

class LaunchCreate(BaseModel):
    title: str
    tagline: str
    description: str

class LaunchResponse(BaseModel):
    id: UUID
    startup_id: UUID
    title: str
    description: str
    upvotes: int
    created_at: datetime

    class Config:
        from_attributes = True
