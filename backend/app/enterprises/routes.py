from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.deps import get_db
from app.core.security import require_role
from app.users.service import get_or_create_user
from app.enterprises.schemas import (
    EnterpriseProfileCreate,
    EnterpriseProfileUpdate,
    EnterpriseProfileResponse,
)
from app.enterprises.service import (
    get_enterprise_profile,
    create_enterprise_profile,
    update_enterprise_profile,
)

router = APIRouter(
    prefix="/enterprise-profile",
    tags=["enterprise-profile"],
)


@router.get(
    "/me",
    response_model=EnterpriseProfileResponse,
)
def get_my_enterprise_profile(
    db: Session = Depends(get_db),
    user=Depends(require_role("enterprise")),
):
    db_user = get_or_create_user(
        db,
        clerk_user_id=user["clerk_user_id"],
        email=user["email"],
        role=user["role"],
    )

    profile = get_enterprise_profile(db, db_user.id)
    if not profile:
        raise HTTPException(status_code=404, detail="Profile not found")

    return profile


@router.post(
    "/me",
    response_model=EnterpriseProfileResponse,
)
def create_my_enterprise_profile(
    payload: EnterpriseProfileCreate,
    db: Session = Depends(get_db),
    user=Depends(require_role("enterprise")),
):
    db_user = get_or_create_user(
        db,
        clerk_user_id=user["clerk_user_id"],
        email=user["email"],
        role=user["role"],
    )

    existing = get_enterprise_profile(db, db_user.id)
    if existing:
        raise HTTPException(status_code=400, detail="Profile already exists")

    return create_enterprise_profile(db, db_user.id, payload)


@router.put(
    "/me",
    response_model=EnterpriseProfileResponse,
)
def update_my_enterprise_profile(
    payload: EnterpriseProfileUpdate,
    db: Session = Depends(get_db),
    user=Depends(require_role("enterprise")),
):
    db_user = get_or_create_user(
        db,
        clerk_user_id=user["clerk_user_id"],
        email=user["email"],
        role=user["role"],
    )

    profile = get_enterprise_profile(db, db_user.id)
    if not profile:
        raise HTTPException(status_code=404, detail="Profile not found")

    return update_enterprise_profile(db, profile, payload)
