# backend/scripts/seed_startups.py

from app.core.database import SessionLocal
from app.users.models import User
from app.startups.models import Startup

# -------------------------------------------------------------------
# REAL INDIAN STARTUP SEED DATA (Demo-grade, enterprise realistic)
# -------------------------------------------------------------------

STARTUP_SEED_DATA = {
    "razorpay@demo.ethaum.ai": {
        "name": "Razorpay",
        "industry": "Fintech / Payments",
        "arr_range": "₹680–850 Cr",
        "description": (
            "Razorpay is a leading full-stack financial services platform in India, "
            "enabling businesses to accept, process, and disburse payments with a "
            "developer-first API approach. It serves startups, SMEs, and large enterprises."
        ),
        "credibility_score": 96,
    },
    "freshworks@demo.ethaum.ai": {
        "name": "Freshworks",
        "industry": "SaaS / CRM & Customer Support",
        "arr_range": "₹240–320 Cr",
        "description": (
            "Freshworks provides cloud-based SaaS solutions for customer engagement, "
            "IT service management, and CRM. Trusted by enterprises globally and "
            "publicly listed on NASDAQ."
        ),
        "credibility_score": 89,
    },
    "chargebee@demo.ethaum.ai": {
        "name": "Chargebee",
        "industry": "SaaS / Billing & Revenue Operations",
        "arr_range": "₹145–180 Cr",
        "description": (
            "Chargebee helps subscription-based businesses manage recurring billing, "
            "invoicing, and revenue recognition at scale. Widely adopted by global SaaS companies."
        ),
        "credibility_score": 88,
    },
    "inmobi@demo.ethaum.ai": {
        "name": "InMobi",
        "industry": "AdTech / Programmatic Advertising",
        "arr_range": "₹280–350 Cr",
        "description": (
            "InMobi is a global mobile advertising and marketing platform delivering "
            "data-driven engagement at scale. It powers mobile-first advertising experiences worldwide."
        ),
        "credibility_score": 87,
    },
    "kale_logistics@demo.ethaum.ai": {
        "name": "Kale Logistics",
        "industry": "SaaS / Logistics & Supply Chain",
        "arr_range": "₹86–110 Cr",
        "description": (
            "Kale Logistics provides digital solutions for air cargo and logistics operations, "
            "helping enterprises streamline supply chain workflows across 40+ countries."
        ),
        "credibility_score": 85,
    },
    "perfios@demo.ethaum.ai": {
        "name": "Perfios",
        "industry": "Fintech / Financial APIs",
        "arr_range": "₹48–65 Cr",
        "description": (
            "Perfios enables financial institutions to automate credit decisioning "
            "through data-driven insights and bank statement analysis APIs."
        ),
        "credibility_score": 82,
    },
    "shipsy@demo.ethaum.ai": {
        "name": "Shipsy",
        "industry": "SaaS / Logistics & Last-Mile Delivery",
        "arr_range": "₹75–95 Cr",
        "description": (
            "Shipsy helps enterprises optimize last-mile delivery and logistics operations "
            "through real-time visibility, routing, and analytics."
        ),
        "credibility_score": 79,
    },
    "vyapar@demo.ethaum.ai": {
        "name": "Vyapar",
        "industry": "SaaS / SME Accounting",
        "arr_range": "₹55–72 Cr",
        "description": (
            "Vyapar is a mobile-first accounting and invoicing platform built for Indian SMEs, "
            "helping small businesses manage billing, GST, and inventory."
        ),
        "credibility_score": 71,
    },
    "esmart_labs@demo.ethaum.ai": {
        "name": "eSmart Labs (Greaves Electric Mobility)",
        "industry": "Climate Tech / EV Infrastructure",
        "arr_range": "₹38–52 Cr",
        "description": (
            "eSmart Labs develops electric vehicle charging and fleet intelligence platforms, "
            "supporting India’s transition to sustainable mobility."
        ),
        "credibility_score": 68,
    },
    "aurassure@demo.ethaum.ai": {
        "name": "Aurassure",
        "industry": "Climate Tech / Renewable Energy",
        "arr_range": "₹4–6.5 Cr",
        "description": (
            "Aurassure is an early-stage climate tech startup focused on solar asset monitoring "
            "and predictive analytics to improve renewable energy efficiency."
        ),
        "credibility_score": 42,
    },
}

# -------------------------------------------------------------------
# SEED EXECUTION
# -------------------------------------------------------------------

def seed_startups():
    db = SessionLocal()
    created_count = 0

    print("\n🚀 Seeding startups...\n")

    for email, data in STARTUP_SEED_DATA.items():
        user = db.query(User).filter(User.email == email).first()

        if not user:
            print(f"⚠️  No user found for {email}, skipping.")
            continue

        existing = db.query(Startup).filter(Startup.user_id == user.id).first()
        if existing:
            print(f"⏭️  Startup already exists for {email}, skipping.")
            continue

        startup = Startup(
            user_id=user.id,
            name=data["name"],
            industry=data["industry"],
            arr_range=data["arr_range"],
            description=data["description"],
            credibility_score=data["credibility_score"],
        )

        db.add(startup)
        db.commit()

        print(f"✅ {data['name']} linked to {email}")
        created_count += 1

    db.close()
    print(f"\n🎉 Phase 2 complete — {created_count} startups created.\n")


if __name__ == "__main__":
    seed_startups()
