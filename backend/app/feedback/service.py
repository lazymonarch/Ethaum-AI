from sqlalchemy.orm import Session
from fastapi import HTTPException
from app.feedback.models import EnterpriseFeedback
from app.startups.credibility import calculate_credibility

def create_feedback(db: Session, startup_id, enterprise_id, data):
    existing = (
        db.query(EnterpriseFeedback)
        .filter(
            EnterpriseFeedback.startup_id == startup_id,
            EnterpriseFeedback.enterprise_id == enterprise_id,
        )
        .first()
    )

    if existing:
        raise HTTPException(
            status_code=409,
            detail="Feedback already submitted for this startup",
        )

    feedback = EnterpriseFeedback(
        startup_id=startup_id,
        enterprise_id=enterprise_id,
        rating=data.rating,
        content=data.content,
        verified=False,
    )

    db.add(feedback)
    db.commit()
    db.refresh(feedback)
    return feedback


def list_verified_feedback(db: Session, startup_id):
    return (
        db.query(EnterpriseFeedback)
        .filter_by(startup_id=startup_id, verified=True)
        .all()
    )


def verify_feedback(db: Session, feedback_id):
    feedback = db.query(EnterpriseFeedback).filter_by(id=feedback_id).first()
    if not feedback:
        return None

    feedback.verified = True
    db.commit()

    result = calculate_credibility(db, feedback.startup)
    feedback.startup.credibility_score = result["overall_score"]
    db.commit()

    return feedback


def get_feedback_by_enterprise(db: Session, enterprise_user_id: int):
    return (
        db.query(EnterpriseFeedback)
        .filter(EnterpriseFeedback.enterprise_id == enterprise_user_id)
        .all()
    )
