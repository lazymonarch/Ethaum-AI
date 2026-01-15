from sqlalchemy.orm import Session
from app.feedback.models import EnterpriseFeedback
from app.startups.credibility import calculate_credibility

def create_feedback(db: Session, startup_id, enterprise_id, data):
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
    
    # Calculate credibility after enterprise feedback verification
    calculate_credibility(db, feedback.startup)
    
    return feedback
