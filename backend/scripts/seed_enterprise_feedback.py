from app.core.database import SessionLocal
from app.startups.models import Startup
from app.feedback.models import EnterpriseFeedback
from app.users.models import User

# -------------------------------------------------------------------
# ENTERPRISE FEEDBACK DATA (High-signal, buyer perspective)
# -------------------------------------------------------------------

FEEDBACK = {
    "Razorpay": [
        (5, "Razorpay is production-grade and enterprise ready. Clear market leader."),
        (5, "Compliance, scale, and support exceeded expectations."),
    ],
    "Freshworks": [
        (4, "Strong value for money with solid AI capabilities."),
        (4, "Works well for mid-to-large enterprises."),
    ],
    "Chargebee": [
        (5, "Excellent billing and revenue automation for SaaS businesses."),
    ],
    "InMobi": [
        (4, "Massive reach and strong audience intelligence."),
    ],
    "Kale Logistics": [
        (4, "Operational visibility improved significantly after adoption."),
    ],
    "Perfios": [
        (4, "Reliable financial data infrastructure for lending use cases."),
    ],
    "Shipsy": [
        (3, "Good logistics optimization, still evolving for complex cases."),
    ],
    "Vyapar": [
        (3, "Useful for SMEs, but limited for enterprise-scale operations."),
    ],
    "eSmart Labs (Greaves Electric Mobility)": [
        (4, "Promising EV infrastructure platform with growing maturity."),
    ],
    "Aurassure": [
        (2, "Early-stage product. Needs more production validation."),
    ],
}

# -------------------------------------------------------------------
# SEED EXECUTION
# -------------------------------------------------------------------

def seed_enterprise_feedback():
    db = SessionLocal()
    created = 0

    print("\n🏢 Seeding enterprise feedback...\n")

    enterprises = db.query(User).filter(User.role == "enterprise").all()
    startups = db.query(Startup).all()

    if not enterprises:
        print("❌ No enterprise users found.")
        return

    for startup in startups:
        entries = FEEDBACK.get(startup.name)
        if not entries:
            print(f"⚠️  No feedback for {startup.name}, skipping.")
            continue

        for i, (rating, text) in enumerate(entries):
            enterprise = enterprises[i % len(enterprises)]

            exists = (
                db.query(EnterpriseFeedback)
                .filter(
                    EnterpriseFeedback.startup_id == startup.id,
                    EnterpriseFeedback.enterprise_id == enterprise.id,
                )
                .first()
            )

            if exists:
                print(f"⏭️  Feedback already exists for {startup.name}")
                continue

            feedback = EnterpriseFeedback(
                startup_id=startup.id,
                enterprise_id=enterprise.id,
                rating=rating,
                content=text,     
                verified=True,
            )

            db.add(feedback)
            db.commit()
            created += 1

            print(
                f"⭐ {startup.name} ← {enterprise.email} "
                f"({rating}/5)"
            )

    db.close()
    print(f"\n🎉 Phase 6 complete — {created} enterprise feedback entries created.\n")


if __name__ == "__main__":
    seed_enterprise_feedback()
