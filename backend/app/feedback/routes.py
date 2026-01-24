from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app.core.deps import get_db
from app.core.security import require_role
from app.users.service import get_or_create_user

from app.feedback.schemas import (
    EnterpriseFeedbackCreate,
    EnterpriseFeedbackResponse,
)
from app.feedback.service import (
    create_feedback,
    get_feedback_by_enterprise,
    list_verified_feedback,
    verify_feedback,
)

router = APIRouter(
    prefix="/enterprise-feedback",
    tags=["enterprise-feedback"],
)

# -------------------------------------------------
# ✅ GET: Feedback submitted by CURRENT enterprise
# -------------------------------------------------
@router.get(
    "/me",
    response_model=List[EnterpriseFeedbackResponse],
)
def get_my_feedback(
    db: Session = Depends(get_db),
    user=Depends(require_role("enterprise")),
):
    db_user = get_or_create_user(
        db=db,
        clerk_user_id=user["clerk_user_id"],
        email=user["email"],
        role=user["role"],
    )

    return get_feedback_by_enterprise(db, db_user.id)


# -------------------------------------------------
# ✅ POST: Submit enterprise feedback (ownership-safe)
# -------------------------------------------------
@router.post(
    "/",
    response_model=EnterpriseFeedbackResponse,
)
def submit_enterprise_feedback(
    payload: EnterpriseFeedbackCreate,
    db: Session = Depends(get_db),
    user=Depends(require_role("enterprise")),
):
    enterprise_user = get_or_create_user(
        db=db,
        clerk_user_id=user["clerk_user_id"],
        email=user["email"],
        role=user["role"],
    )

    return create_feedback(
        db=db,
        startup_id=payload.startup_id,
        enterprise_id=enterprise_user.id,
        data=payload,
    )


# -------------------------------------------------
# 🌍 GET: Public verified feedback for a startup
# -------------------------------------------------
@router.get(
    "/startup/{startup_id}",
    response_model=List[EnterpriseFeedbackResponse],
)
def get_public_enterprise_feedback(
    startup_id: str,
    db: Session = Depends(get_db),
):
    return list_verified_feedback(db, startup_id)


# -------------------------------------------------
# 🛡️ POST: Admin verifies enterprise feedback
# -------------------------------------------------
@router.post(
    "/{feedback_id}/verify",
    response_model=EnterpriseFeedbackResponse,
)
def admin_verify_enterprise_feedback(
    feedback_id: str,
    db: Session = Depends(get_db),
    user=Depends(require_role("admin")),
):
    feedback = verify_feedback(db, feedback_id)

    if not feedback:
        raise HTTPException(
            status_code=404,
            detail="Feedback not found",
        )

    return feedback
