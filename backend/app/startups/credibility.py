import math
from sqlalchemy.orm import Session

from app.launches.models import Launch
from app.reviews.models import Review
from app.feedback.models import EnterpriseFeedback
from app.startups.models import Startup


def calculate_profile_completeness(startup: Startup) -> int:
    """
    Calculate profile completeness with basic quality checks.
    """
    checks = [
        bool(startup.name and len(startup.name) > 2),
        bool(startup.industry),
        bool(startup.arr_range),
        bool(startup.description and len(startup.description) > 20),
    ]
    filled = sum(checks)
    return int((filled / len(checks)) * 100)


def calculate_credibility(db: Session, startup: Startup) -> dict:
    """
    Calculate an explainable credibility score for a startup.

    Weights:
    - Launch Engagement: 25%
    - Verified Reviews: 25%
    - Enterprise Feedback: 30%
    - Profile Completeness: 20%
    """

    # ─────────────────────────────
    # 1. Launch Engagement (25%)
    # ─────────────────────────────
    launches = db.query(Launch).filter_by(startup_id=startup.id).all()
    total_upvotes = sum(l.upvotes for l in launches)

    if total_upvotes > 0:
        # Logarithmic scaling with diminishing returns
        launch_score = min(
            int(math.log(total_upvotes + 1, 1.3) * 15),
            100
        )
    else:
        launch_score = 0

    # ─────────────────────────────
    # 2. Verified Reviews (25%)
    # ─────────────────────────────
    verified_reviews_count = (
        db.query(Review)
        .filter_by(startup_id=startup.id, verified=True)
        .count()
    )

    # 10 reviews → max score
    review_score = min(verified_reviews_count * 10, 100)

    # ─────────────────────────────
    # 3. Enterprise Feedback (30%)
    # ─────────────────────────────
    verified_feedback = (
        db.query(EnterpriseFeedback)
        .filter_by(startup_id=startup.id, verified=True)
        .all()
    )

    if verified_feedback:
        avg_rating = sum(f.rating for f in verified_feedback) / len(verified_feedback)
        feedback_count = len(verified_feedback)

        # Quality from rating
        base_score = int((avg_rating / 5) * 100)

        # Confidence multiplier (full confidence at 3+ feedbacks)
        confidence = min(feedback_count / 3.0, 1.0)

        enterprise_score = int(base_score * confidence)
    else:
        enterprise_score = 0

    # ─────────────────────────────
    # 4. Profile Completeness (20%)
    # ─────────────────────────────
    profile_score = calculate_profile_completeness(startup)

    # ─────────────────────────────
    # Final Weighted Score
    # ─────────────────────────────
    final_score = int(
        launch_score * 0.25 +
        review_score * 0.25 +
        enterprise_score * 0.30 +
        profile_score * 0.20
    )

    # Check if startup has enough data to be meaningfully scored
    has_data = (
        total_upvotes > 0
        or verified_reviews_count > 0
        or len(verified_feedback) > 0
    )

    breakdown = {
        "launch_engagement": launch_score,
        "verified_reviews": review_score,
        "enterprise_feedback": enterprise_score,
        "profile_completeness": profile_score,
        "final_score": final_score,
        "insufficient_data": not has_data,
        "metadata": {
            "total_upvotes": total_upvotes,
            "verified_reviews_count": verified_reviews_count,
            "enterprise_feedback_count": len(verified_feedback),
            "avg_enterprise_rating": (
                round(
                    sum(f.rating for f in verified_feedback) / len(verified_feedback),
                    1
                ) if verified_feedback else None
            ),
        },
    }

    # Persist final score
    startup.credibility_score = final_score
    db.commit()

    return breakdown
