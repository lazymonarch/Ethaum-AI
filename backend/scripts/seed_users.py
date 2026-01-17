# backend/scripts/seed_users.py

from sqlalchemy.orm import Session
from app.core.database import SessionLocal
from app.users.models import User
import uuid


# ─────────────────────────────
# Seed data definitions
# ─────────────────────────────

ADMIN_USER = {
    "clerk_user_id": "admin_demo_001",
    "email": "admin@ethaum.ai",
    "role": "admin",
}

STARTUP_USERS = [
    "razorpay",
    "freshworks",
    "chargebee",
    "inmobi",
    "kale_logistics",
    "perfios",
    "shipsy",
    "vyapar",
    "esmart_labs",
    "aurassure",
]

ENTERPRISE_USERS = [
    "enterprise_alpha",
    "enterprise_beta",
    "enterprise_gamma",
    "enterprise_delta",
    "enterprise_epsilon",
    "enterprise_zeta",
]


# ─────────────────────────────
# Helpers
# ─────────────────────────────

def create_user(db: Session, clerk_user_id: str, email: str, role: str):
    existing = (
        db.query(User)
        .filter(User.clerk_user_id == clerk_user_id)
        .first()
    )
    if existing:
        print(f"⚠️ User already exists: {email}")
        return existing

    user = User(
        id=uuid.uuid4(),
        clerk_user_id=clerk_user_id,
        email=email,
        role=role,
    )
    db.add(user)
    db.commit()
    db.refresh(user)

    print(f"✅ Created {role} user: {email}")
    return user


# ─────────────────────────────
# Main seeding logic
# ─────────────────────────────

def seed_users():
    db = SessionLocal()

    try:
        print("\n🚀 Seeding users...\n")

        # Admin
        create_user(
            db,
            ADMIN_USER["clerk_user_id"],
            ADMIN_USER["email"],
            ADMIN_USER["role"],
        )

        # Startup users
        for name in STARTUP_USERS:
            create_user(
                db,
                clerk_user_id=f"startup_{name}",
                email=f"{name}@demo.ethaum.ai",
                role="startup",
            )

        # Enterprise users
        for name in ENTERPRISE_USERS:
            create_user(
                db,
                clerk_user_id=f"{name}",
                email=f"{name}@enterprise.demo",
                role="enterprise",
            )

        print("\n🎉 User seeding complete.\n")

    finally:
        db.close()


if __name__ == "__main__":
    seed_users()
