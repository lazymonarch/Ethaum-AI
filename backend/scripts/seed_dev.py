import os
import random
import sys
from typing import List

from dotenv import load_dotenv
from sqlalchemy.orm import Session

# -------------------------------------------------
# ENV + PATH SETUP
# -------------------------------------------------
load_dotenv()
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from app.core.database import SessionLocal
from app.users.service import get_or_create_user
from app.startups.models import Startup
from app.enterprises.models import EnterpriseProfile
from app.launches.models import Launch
from app.reviews.models import Review
from app.feedback.models import EnterpriseFeedback
from app.startups.credibility import calculate_credibility

from clerk_backend_api import Clerk

# -------------------------------------------------
# CONFIG
# -------------------------------------------------
PASSWORD = "lakshan1705"

ADMIN_EMAIL = "admin@ethaum.dev"

ENTERPRISE_EMAILS = [
    "enterprise1@ethaum.dev",
    "enterprise2@ethaum.dev",
    "enterprise3@ethaum.dev",
]

STARTUP_EMAILS = [f"startup{i}@ethaum.dev" for i in range(1, 21)]

INDUSTRIES = ["Fintech", "SaaS", "AI", "Healthtech", "E-commerce"]
ARR_RANGES = ["0-5 Cr", "5-25 Cr", "25-100 Cr", "100+ Cr"]

LOW_COUNT = 6
MID_COUNT = 8
HIGH_COUNT = 6

# -------------------------------------------------
# CLERK INIT
# -------------------------------------------------
CLERK_SECRET_KEY = os.getenv("CLERK_SECRET_KEY")
if not CLERK_SECRET_KEY:
    raise RuntimeError("❌ CLERK_SECRET_KEY missing")

clerk = Clerk(bearer_auth=CLERK_SECRET_KEY)

# -------------------------------------------------
# CLERK HELPERS (MINIMAL SDK SAFE)
# -------------------------------------------------
def get_or_create_clerk_user(email: str, role: str):
    # 1️⃣ Try to find existing user
    users = clerk.users.list()
    for u in users:
        for e in u.email_addresses:
            if e.email_address == email:
                return u

    print(f"➕ Creating Clerk user: {email} ({role})")

    # 2️⃣ Create user (email must be string)
    user = clerk.users.create(
        email_address=[email],
        password=PASSWORD,
        skip_password_checks=True,
        unsafe_metadata={"role": role},
    )

    # 3️⃣ Mark email as VERIFIED (DEV only)
    clerk.email_addresses.update(
        email_address_id=user.primary_email_address_id,
        verified=True,
    )

    return user


# -------------------------------------------------
# DB SEED HELPERS
# -------------------------------------------------
def seed_enterprise_profile(db: Session, user_id: str):
    profile = db.query(EnterpriseProfile).filter_by(user_id=user_id).first()
    if profile:
        return profile

    profile = EnterpriseProfile(
        user_id=user_id,
        company_name="Enterprise Corp",
        industry=random.choice(INDUSTRIES),
        company_size=random.choice(["50-200", "200-500", "500+"]),
        location="India",
        interested_industries=random.sample(INDUSTRIES, 2),
        preferred_arr_ranges=random.sample(ARR_RANGES, 2),
        engagement_stage="Evaluation",
    )
    db.add(profile)
    db.commit()
    return profile


def seed_startup(db: Session, user_id: str, idx: int):
    startup = db.query(Startup).filter_by(user_id=user_id).first()
    if startup:
        return startup

    startup = Startup(
        user_id=user_id,
        name=f"Startup {idx}",
        industry=INDUSTRIES[idx % len(INDUSTRIES)],
        arr_range=ARR_RANGES[idx % len(ARR_RANGES)],
        description=f"Startup {idx} is building innovative solutions in {INDUSTRIES[idx % len(INDUSTRIES)]}.",
        credibility_score=0,
    )
    db.add(startup)
    db.commit()
    return startup


def seed_launches(db: Session, startup: Startup, count: int):
    existing = db.query(Launch).filter_by(startup_id=startup.id).count()
    if existing >= count:
        return

    for i in range(count - existing):
        db.add(
            Launch(
                startup_id=startup.id,
                title=f"{startup.name} Launch {i+1}",
                tagline="Revolutionary product",
                description="This product changes everything.",
                upvotes=random.randint(50, 400),
            )
        )
    db.commit()


def seed_reviews(
    db: Session,
    startup: Startup,
    reviewer_user_id: str,
    count: int,
    verified_ratio=0.5,
):
    for _ in range(count):
        review = Review(
            startup_id=startup.id,
            user_id=reviewer_user_id,  
            reviewer_role="customer",
            content="Great product!",
            verified=random.random() < verified_ratio,
        )
        db.add(review)
    db.commit()



def seed_enterprise_feedback(
    db: Session,
    startup: Startup,
    enterprise_ids: List[str],
):
    existing = db.query(EnterpriseFeedback).filter_by(startup_id=startup.id).count()
    if existing > 0:
        return

    sampled = random.sample(enterprise_ids, min(2, len(enterprise_ids)))
    for ent_id in sampled:
        db.add(
            EnterpriseFeedback(
                startup_id=startup.id,
                enterprise_id=ent_id,
                rating=random.randint(4, 5),
                content="Strong enterprise fit",
                verified=True,
            )
        )
    db.commit()

# -------------------------------------------------
# MAIN
# -------------------------------------------------
def main():
    print("🚀 Seeding EthAum DEV database...")
    db = SessionLocal()

    # ADMIN
    admin_clerk = get_or_create_clerk_user(ADMIN_EMAIL, "admin")
    admin_db = get_or_create_user(
    db,
    clerk_user_id=admin_clerk.id,
    email=ADMIN_EMAIL,
    role="admin",
    )


    # ENTERPRISES
    enterprise_db_ids = []
    for email in ENTERPRISE_EMAILS:
        cu = get_or_create_clerk_user(email, "enterprise")
        du = get_or_create_user(db, cu.id, email, "enterprise")
        seed_enterprise_profile(db, du.id)
        enterprise_db_ids.append(du.id)

    # STARTUPS
    startups = []
    for idx, email in enumerate(STARTUP_EMAILS):
        cu = get_or_create_clerk_user(email, "startup")
        du = get_or_create_user(db, cu.id, email, "startup")
        startups.append(seed_startup(db, du.id, idx + 1))

    # TIERS
    low = startups[:LOW_COUNT]
    mid = startups[LOW_COUNT : LOW_COUNT + MID_COUNT]
    high = startups[-HIGH_COUNT:]

    for s in mid:
        seed_launches(db, s, 1)
        seed_reviews(db, s, admin_db.id, 2)

    for s in high:
        seed_launches(db, s, 3)
        seed_reviews(db, s, admin_db.id, 4, verified_ratio=0.8)
        seed_enterprise_feedback(db, s, enterprise_db_ids)

    # RECALCULATE
    for s in startups:
        calculate_credibility(db, s)

    print("✅ Seeding complete.")
    print(f"🔐 Login password for ALL users: {PASSWORD}")
    db.close()


if __name__ == "__main__":
    main()
