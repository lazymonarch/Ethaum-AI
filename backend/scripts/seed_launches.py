# backend/scripts/seed_launches.py

from app.core.database import SessionLocal
from app.startups.models import Startup
from app.launches.models import Launch

# -------------------------------------------------------------------
# LAUNCH SEED DATA (Enterprise-grade, realistic)
# -------------------------------------------------------------------

LAUNCHES = {
    "Razorpay": [
        (
            "Razorpay Smart Collect",
            "Automated collections platform enabling enterprises to manage recurring payments, "
            "virtual accounts, and reconciliation at scale."
        ),
        (
            "Razorpay Route",
            "A payment routing solution for marketplaces and platforms to split settlements "
            "between vendors with full compliance."
        ),
    ],
    "Freshworks": [
        (
            "Freddy AI for CX",
            "An AI-powered assistant that helps enterprises automate customer support, "
            "predict intent, and resolve tickets faster."
        ),
        (
            "Freshservice Neo",
            "Next-generation ITSM platform with workflow automation and analytics "
            "built for modern enterprise IT teams."
        ),
    ],
    "Chargebee": [
        (
            "Chargebee RevRec",
            "Automated revenue recognition solution built to support ASC 606 "
            "and IFRS compliance for SaaS companies."
        ),
        (
            "Chargebee Retention",
            "A churn prevention and subscription retention platform using "
            "payment recovery and lifecycle insights."
        ),
    ],
    "InMobi": [
        (
            "InMobi Exchange",
            "A global programmatic advertising exchange delivering high-quality "
            "mobile inventory for enterprise advertisers."
        ),
        (
            "InMobi Audiences",
            "An AI-driven audience intelligence platform enabling precise "
            "targeting at massive scale."
        ),
    ],
    "Kale Logistics": [
        (
            "Cargo Community System",
            "A digital ecosystem connecting airlines, freight forwarders, "
            "and airports to streamline cargo operations."
        ),
        (
            "Airport Cargo Operations",
            "An end-to-end cargo management platform improving visibility "
            "and efficiency for airport authorities."
        ),
    ],
    "Perfios": [
        (
            "Bank Statement Analyzer",
            "Automated financial analysis engine used by banks and NBFCs "
            "to accelerate credit underwriting."
        ),
        (
            "Perfios Data Platform",
            "Unified data ingestion platform supporting GST, bank, "
            "and financial document analytics."
        ),
    ],
    "Shipsy": [
        (
            "Last-Mile Intelligence Suite",
            "AI-powered route optimization and real-time tracking platform "
            "for enterprise logistics teams."
        ),
        (
            "Control Tower",
            "Centralized logistics command center providing end-to-end "
            "shipment visibility and analytics."
        ),
    ],
    "Vyapar": [
        (
            "Vyapar GST Billing",
            "GST-compliant billing and invoicing solution tailored for "
            "Indian SMEs and distributors."
        ),
        (
            "Vyapar Inventory Pro",
            "Inventory and accounting management tool designed for "
            "offline-first business workflows."
        ),
    ],
    "eSmart Labs (Greaves Electric Mobility)": [
        (
            "EV Fleet Intelligence",
            "Fleet analytics platform providing real-time insights into "
            "electric vehicle performance and utilization."
        ),
        (
            "Charging Network OS",
            "Software platform for managing large-scale EV charging "
            "infrastructure across urban regions."
        ),
    ],
    "Aurassure": [
        (
            "Solar Asset Monitoring",
            "IoT-enabled monitoring system providing real-time health "
            "and performance analytics for solar installations."
        ),
        (
            "Predictive Maintenance Engine",
            "AI-driven maintenance forecasting tool aimed at improving "
            "uptime of renewable energy assets."
        ),
    ],
}

# -------------------------------------------------------------------
# SEED EXECUTION
# -------------------------------------------------------------------

def generate_tagline(title: str, description: str) -> str:
    """
    Generate a short, non-null tagline.
    Guaranteed to return a valid string.
    """
    if description:
        if "." in description:
            tagline = description.split(".")[0].strip()
        else:
            tagline = description.strip()[:100]
    else:
        tagline = title

    # absolute safety fallback
    if not tagline:
        tagline = title

    # limit length defensively
    return tagline[:120]


def seed_launches():
    db = SessionLocal()
    created = 0

    print("\n🚀 Seeding launches...\n")

    startups = db.query(Startup).all()

    for startup in startups:
        startup_launches = LAUNCHES.get(startup.name)

        if not startup_launches:
            print(f"⚠️  No launch data for {startup.name}, skipping.")
            continue

        for title, description in startup_launches:
            exists = (
                db.query(Launch)
                .filter(
                    Launch.startup_id == startup.id,
                    Launch.title == title,
                )
                .first()
            )

            if exists:
                print(f"⏭️  Launch already exists: {title}")
                continue

            tagline = generate_tagline(title, description)

            launch = Launch(
                startup_id=startup.id,
                title=title,
                tagline=tagline,          
                description=description,
                upvotes=0,
                featured=False,
            )

            db.add(launch)
            db.commit()
            created += 1

            print(f"✅ {startup.name} → {title}")

    db.close()
    print(f"\n🎉 Phase 3 complete — {created} launches created.\n")


if __name__ == "__main__":
    seed_launches()
