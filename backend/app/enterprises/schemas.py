from pydantic import BaseModel
from typing import List, Optional
from uuid import UUID


class EnterpriseProfileBase(BaseModel):
    company_name: str
    industry: str
    company_size: str
    location: str

    interested_industries: List[str]
    preferred_arr_ranges: List[str]

    engagement_stage: Optional[str] = None


class EnterpriseProfileCreate(EnterpriseProfileBase):
    pass


class EnterpriseProfileUpdate(BaseModel):
    company_name: Optional[str] = None
    industry: Optional[str] = None
    company_size: Optional[str] = None
    location: Optional[str] = None

    interested_industries: Optional[List[str]] = None
    preferred_arr_ranges: Optional[List[str]] = None
    engagement_stage: Optional[str] = None


class EnterpriseProfileResponse(EnterpriseProfileBase):
    id: UUID
    user_id: UUID

    class Config:
        from_attributes = True
