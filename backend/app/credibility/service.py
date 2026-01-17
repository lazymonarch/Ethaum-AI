# app/credibility/service.py

from sqlalchemy.orm import Session
from datetime import datetime

from app.startups.models import Startup
from app.launches.models import Launch
from app.reviews.models import Review
from app.feedback.models import EnterpriseFeedback


# -------------------------------------------------
# SCORING HELPERS
# -------------------------------------------------

def calculate_launch_score(total_upvotes: int) -> int:
    if total_upvotes >= 1500:
        return 25
    if total_upvotes >= 1000:
        return 22
    if total_upvotes >= 500:
        return 18
    if total_upvotes >= 200:
        return 12
    if total_upvotes > 0:
        return 6
    return 0


def calculate_review_score(verified: int, unverified: int) -> int:
    score = (verified * 6) + (unverified * 2)
    return min(score, 25)


def calculate_enterprise_score(avg_rating: float | None) -> int:
    if not avg_rating:
        return 0
    return int((avg_rating / 5) * 30)


def calculate_profile_score(startup: Startup):
    required_fields = ["name", "industry", "arr_range", "description"]
    missing = [f for f in required_fields if not getattr(startup, f)]
    if not missing:
        return 20, []
    if len(missing) <= 1:
        return 10, missing
    return 0, missing


# -------------------------------------------------
# MAIN SERVICE
# -------------------------------------------------

def get_credibility_score(db: Session, startup_id):
    startup = db.query(Startup).filter(Startup.id == startup_id).first()
    if not startup:
        return None

    # -------------------------------
    # Launch Engagement
    # -------------------------------
    launches = db.query(Launch).filter(Launch.startup_id == startup.id).all()
    total_upvotes = sum(l.upvotes for l in launches)
    launch_score = calculate_launch_score(total_upvotes)

    # -------------------------------
    # Reviews
    # -------------------------------
    reviews = db.query(Review).filter(Review.startup_id == startup.id).all()
    verified_reviews = sum(1 for r in reviews if r.verified)
    unverified_reviews = sum(1 for r in reviews if not r.verified)
    review_score = calculate_review_score(verified_reviews, unverified_reviews)

    # -------------------------------
    # Enterprise Feedback
    # -------------------------------
    feedback = (
        db.query(EnterpriseFeedback)
        .filter(EnterpriseFeedback.startup_id == startup.id)
        .all()
    )

    if feedback:
        avg_rating = sum(f.rating for f in feedback) / len(feedback)
    else:
        avg_rating = None

    enterprise_score = calculate_enterprise_score(avg_rating)

    # -------------------------------
    # Profile Completeness
    # -------------------------------
    profile_score, missing_fields = calculate_profile_score(startup)

    # -------------------------------
    # Final Score
    # -------------------------------
    overall_score = (
        launch_score
        + review_score
        + enterprise_score
        + profile_score
    )

    return {
        "startup_id": str(startup.id),
        "overall_score": overall_score,
        "breakdown": {
            "launch_engagement": {
                "score": launch_score,
                "max": 25,
                "details": {
                    "total_upvotes": total_upvotes,
                    "launch_count": len(launches),
                },
            },
            "peer_reviews": {
                "score": review_score,
                "max": 25,
                "details": {
                    "total_reviews": len(reviews),
                    "verified_reviews": verified_reviews,
                },
            },
            "enterprise_feedback": {
                "score": enterprise_score,
                "max": 30,
                "details": {
                    "avg_rating": avg_rating,
                    "feedback_count": len(feedback),
                },
            },
            "profile_completeness": {
                "score": profile_score,
                "max": 20,
                "details": {
                    "missing_fields": missing_fields,
                },
            },
        },
        "last_updated": datetime.utcnow(),
    }
