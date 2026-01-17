from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.deps import get_db
from app.core.security import require_role
from app.startups.service import get_startup_by_user
from app.users.service import get_or_create_user
from app.reviews.schemas import ReviewCreate, ReviewResponse
from app.reviews.service import create_review, list_verified_reviews, verify_review

router = APIRouter(prefix="/reviews", tags=["reviews"])

@router.post("/", response_model=ReviewResponse)
def submit_review(
    payload: ReviewCreate,
    db: Session = Depends(get_db),
    user=Depends(require_role("startup")),
):
    db_user = get_or_create_user(
        db,
        clerk_user_id=user["clerk_user_id"],
        email=user.get("email", "unknown@example.com"),
        role=user["role"],
    )

    startup = get_startup_by_user(db, db_user.id)
    if not startup:
        raise HTTPException(status_code=400, detail="Startup not found")

    review = create_review(
        db=db,
        startup_id=startup.id,
        user_id=db_user.id,
        reviewer_role="startup",
        content=payload.content,
    )

    return review


@router.get("/startup/{startup_id}", response_model=list[ReviewResponse])
def get_public_reviews(startup_id: str, db: Session = Depends(get_db)):
    return list_verified_reviews(db, startup_id)


@router.post("/{review_id}/verify", response_model=ReviewResponse)
def admin_verify_review(
    review_id: str,
    db: Session = Depends(get_db),
    user=Depends(require_role("admin")),
):
    review = verify_review(db, review_id)
    if not review:
        raise HTTPException(status_code=404, detail="Review not found")
    return review
