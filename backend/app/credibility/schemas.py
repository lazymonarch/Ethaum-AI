# app/credibility/schemas.py

from pydantic import BaseModel
from typing import List, Optional, Dict
from datetime import datetime


class ScoreDetails(BaseModel):
    score: int
    max: int
    details: Dict


class CredibilityBreakdown(BaseModel):
    launch_engagement: ScoreDetails
    peer_reviews: ScoreDetails
    enterprise_feedback: ScoreDetails
    profile_completeness: ScoreDetails


class CredibilityScoreResponse(BaseModel):
    startup_id: str
    overall_score: int
    breakdown: CredibilityBreakdown
    last_updated: datetime
