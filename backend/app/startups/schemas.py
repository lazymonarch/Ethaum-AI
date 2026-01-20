from pydantic import BaseModel
from uuid import UUID
from datetime import datetime
from enum import Enum


class ARRRange(str, Enum):
    zero_to_five = "0-5 Cr"
    five_to_twenty_five = "5-25 Cr"
    twenty_five_to_hundred = "25-100 Cr"
    hundred_plus = "100+ Cr"


class StartupCreate(BaseModel):
    name: str
    industry: str
    arr_range: ARRRange
    description: str


class StartupResponse(BaseModel):
    id: UUID
    name: str
    industry: str
    arr_range: str
    description: str
    credibility_score: int | None
    created_at: datetime

    class Config:
        from_attributes = True
