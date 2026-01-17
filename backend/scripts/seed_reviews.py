# backend/scripts/seed_reviews.py

from app.core.database import SessionLocal
from app.startups.models import Startup
from app.reviews.models import Review
from app.users.models import User

# -------------------------------------------------------------------
# REVIEW SEED DATA (Enterprise-grade, opinionated)
# -------------------------------------------------------------------

REVIEWS = {
    "Razorpay": [
        ("enterprise", True, "Razorpay has significantly simplified our payment reconciliation across multiple business units."),
        ("enterprise", True, "Their APIs are stable and enterprise-ready. We scaled to millions of transactions without issues."),
        ("enterprise", True, "Excellent compliance support and responsiveness from their enterprise team."),
        ("customer", False, "Integrations were smooth, documentation is very clear."),
    ],
    "Freshworks": [
        ("enterprise", True, "Freddy AI reduced our ticket resolution time by nearly 40%."),
        ("enterprise", True, "Freshservice fits well into modern IT workflows."),
        ("customer", False, "Easy to onboard teams and configure automations."),
    ],
    "Chargebee": [
        ("enterprise", True, "Revenue recognition automation saved our finance team weeks of effort."),
        ("enterprise", True, "Retention workflows noticeably improved churn recovery."),
        ("customer", False, "Billing flows are flexible and well-documented."),
    ],
    "InMobi": [
        ("enterprise", True, "The scale and reach of InMobi Exchange is unmatched."),
        ("enterprise", True, "Audience intelligence capabilities are very strong."),
        ("customer", False, "Campaign performance was better than expected."),
    ],
    "Kale Logistics": [
        ("enterprise", True, "Cargo operations became significantly more transparent."),
        ("customer", False, "Reduced coordination overhead across partners."),
    ],
    "Perfios": [
        ("enterprise", True, "Perfios APIs accelerated our credit decisioning pipeline."),
        ("customer", False, "Data ingestion accuracy is impressive."),
    ],
    "Shipsy": [
        ("enterprise", True, "Route optimization led to measurable cost savings."),
        ("customer", False, "Control Tower dashboards are very useful."),
    ],
    "Vyapar": [
        ("customer", False, "Very practical for SME billing and inventory management."),
    ],
    "eSmart Labs (Greaves Electric Mobility)": [
        ("enterprise", True, "Fleet intelligence insights helped optimize EV utilization."),
        ("customer", False, "Charging network management is improving steadily."),
    ],
    "Aurassure": [
        ("customer", False, "Promising product, but still early in maturity."),
    ],
}

# -------------------------------------------------------------------
# SEED EXECUTION
# -------------------------------------------------------------------

def seed_reviews():
    db = SessionLocal()
    created = 0

    print("\n📝 Seeding reviews...\n")

    startups = db.query(Startup).all()

    for startup in startups:
        startup_reviews = REVIEWS.get(startup.name)

        if not startup_reviews:
            print(f"⚠️  No reviews configured for {startup.name}, skipping.")
            continue

        for reviewer_role, verified, content in startup_reviews:
            # Pick any user with matching role
            user = (
                db.query(User)
                .filter(User.role == reviewer_role)
                .first()
            )

            if not user:
                print(f"⚠️  No user found for role {reviewer_role}, skipping review.")
                continue

            exists = (
                db.query(Review)
                .filter(
                    Review.startup_id == startup.id,
                    Review.content == content
                )
                .first()
            )

            if exists:
                print("⏭️  Review already exists, skipping.")
                continue

            review = Review(
                startup_id=startup.id,
                user_id=user.id,
                reviewer_role=reviewer_role,
                content=content,
                verified=verified,
            )

            db.add(review)
            db.commit()
            created += 1

            badge = "✅ VERIFIED" if verified else "🟡 UNVERIFIED"
            print(f"{badge} {startup.name}: {content[:50]}...")

    db.close()
    print(f"\n🎉 Phase 5 complete — {created} reviews created.\n")


if __name__ == "__main__":
    seed_reviews()
