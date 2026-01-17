# app/credibility/routes.py

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.deps import get_db
from app.core.security import get_current_user
from app.credibility.schemas import CredibilityScoreResponse
from app.credibility.service import get_credibility_score
from app.startups.service import get_startup_by_user
from app.users.service import get_or_create_user 

router = APIRouter(prefix="/credibility-score", tags=["Credibility"])


# -----------------------------------
# Startup viewing their own score
# -----------------------------------
@router.get("/", response_model=CredibilityScoreResponse)
def my_credibility_score(
    db: Session = Depends(get_db),
    user=Depends(get_current_user),
):
    db_user = get_or_create_user(
        db,
        clerk_user_id=user["clerk_user_id"],
        email=user["email"],
        role=user["role"],
    )
    startup = get_startup_by_user(db, db_user.id)
    if not startup:
        raise HTTPException(status_code=404, detail="Startup not found")

    result = get_credibility_score(db, startup.id)
    return result


# -----------------------------------
# Enterprise viewing a startup
# -----------------------------------
@router.get("/{startup_id}", response_model=CredibilityScoreResponse)
def startup_credibility_score(
    startup_id: str,
    db: Session = Depends(get_db),
):
    result = get_credibility_score(db, startup_id)
    if not result:
        raise HTTPException(status_code=404, detail="Startup not found")

    return result
