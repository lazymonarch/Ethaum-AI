from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.deps import get_db
from app.core.security import require_role
from app.users.service import get_or_create_user
from app.feedback.schemas import (
    EnterpriseFeedbackCreate,
    EnterpriseFeedbackResponse,
)
from app.feedback.service import (
    create_feedback,
    list_verified_feedback,
    verify_feedback,
)

router = APIRouter(prefix="/enterprise-feedback", tags=["enterprise-feedback"])

@router.post("/", response_model=EnterpriseFeedbackResponse)
def submit_enterprise_feedback(
    payload: EnterpriseFeedbackCreate,
    db: Session = Depends(get_db),
    user=Depends(require_role("enterprise")),
):
    enterprise_user = get_or_create_user(
        db,
        clerk_user_id=user["clerk_user_id"],
        email=user.get("email", "unknown@example.com"),
        role=user["role"],
    )

    return create_feedback(
        db,
        startup_id=payload.startup_id,
        enterprise_id=enterprise_user.id,
        data=payload,
    )


@router.get("/startup/{startup_id}", response_model=list[EnterpriseFeedbackResponse])
def get_public_enterprise_feedback(
    startup_id: str,
    db: Session = Depends(get_db),
):
    return list_verified_feedback(db, startup_id)


@router.post("/{feedback_id}/verify", response_model=EnterpriseFeedbackResponse)
def admin_verify_enterprise_feedback(
    feedback_id: str,
    db: Session = Depends(get_db),
    user=Depends(require_role("admin")),
):
    feedback = verify_feedback(db, feedback_id)
    if not feedback:
        raise HTTPException(status_code=404, detail="Feedback not found")
    return feedback
