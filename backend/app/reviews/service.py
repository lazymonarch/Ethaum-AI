from sqlalchemy.orm import Session
from app.reviews.models import Review
from app.startups.credibility import calculate_credibility
from uuid import UUID

def create_review(
    db: Session,
    startup_id: UUID,
    user_id: UUID,
    reviewer_role: str,
    content: str,
):
    review = Review(
        startup_id=startup_id,
        user_id=user_id,   
        reviewer_role=reviewer_role,
        content=content,
        verified=False,
    )

    db.add(review)
    db.commit()
    db.refresh(review)
    return review


def list_verified_reviews(db: Session, startup_id):
    return (
        db.query(Review)
        .filter_by(startup_id=startup_id, verified=True)
        .all()
    )


def verify_review(db: Session, review_id):
    review = db.query(Review).filter_by(id=review_id).first()
    if not review:
        return None
    review.verified = True
    db.commit()
    
    calculate_credibility(db, review.startup)
    
    return review
