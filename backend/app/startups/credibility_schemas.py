from pydantic import BaseModel
from typing import Optional, Dict


class CredibilityOut(BaseModel):
    launch_engagement: int
    verified_reviews: int
    enterprise_feedback: int
    profile_completeness: int
    final_score: int
    insufficient_data: bool
    metadata: Dict[str, Optional[float]]
