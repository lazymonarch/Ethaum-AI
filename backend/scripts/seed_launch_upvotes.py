# backend/scripts/seed_launch_upvotes.py

from app.core.database import SessionLocal
from app.launches.models import Launch
from app.startups.models import Startup

# -------------------------------------------------------------------
# UPVOTE DISTRIBUTION (Realistic, deterministic)
# -------------------------------------------------------------------

UPVOTE_MAP = {
    "Razorpay": [1450, 1200],
    "Freshworks": [980, 860],
    "Chargebee": [720, 640],
    "InMobi": [680, 590],
    "Kale Logistics": [420, 360],
    "Perfios": [310, 260],
    "Shipsy": [240, 190],
    "Vyapar": [210, 170],
    "eSmart Labs (Greaves Electric Mobility)": [140, 110],
    "Aurassure": [55, 35],
}

# -------------------------------------------------------------------
# SEED EXECUTION
# -------------------------------------------------------------------

def seed_launch_upvotes():
    db = SessionLocal()
    updated = 0

    print("\n🔥 Seeding launch upvotes...\n")

    startups = db.query(Startup).all()

    for startup in startups:
        vote_pattern = UPVOTE_MAP.get(startup.name)

        if not vote_pattern:
            print(f"⚠️  No upvote config for {startup.name}, skipping.")
            continue

        launches = (
            db.query(Launch)
            .filter(Launch.startup_id == startup.id)
            .order_by(Launch.created_at.asc())
            .all()
        )

        for idx, launch in enumerate(launches):
            # cap index to avoid overflow
            upvotes = vote_pattern[min(idx, len(vote_pattern) - 1)]

            launch.upvotes = upvotes
            updated += 1

            print(f"👍 {startup.name} → {launch.title}: {upvotes} upvotes")

        db.commit()

    db.close()
    print(f"\n🎉 Phase 4 complete — {updated} launches updated.\n")


if __name__ == "__main__":
    seed_launch_upvotes()
