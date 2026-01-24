from sqlalchemy.orm import Session
from app.enterprises.models import EnterpriseProfile
from app.enterprises.schemas import (
    EnterpriseProfileCreate,
    EnterpriseProfileUpdate,
)


def get_enterprise_profile(db: Session, user_id):
    return (
        db.query(EnterpriseProfile)
        .filter(EnterpriseProfile.user_id == user_id)
        .first()
    )


def create_enterprise_profile(
    db: Session,
    user_id,
    payload: EnterpriseProfileCreate,
):
    profile = EnterpriseProfile(
        user_id=user_id,
        **payload.model_dump(),
    )

    db.add(profile)
    db.commit()
    db.refresh(profile)
    return profile


def update_enterprise_profile(
    db: Session,
    profile: EnterpriseProfile,
    payload: EnterpriseProfileUpdate,
):
    for field, value in payload.model_dump(exclude_unset=True).items():
        setattr(profile, field, value)

    db.commit()
    db.refresh(profile)
    return profile
