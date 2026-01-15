from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.deps import get_db
from app.core.security import get_current_user, require_role
from app.users.service import get_or_create_user
from app.startups.schemas import StartupCreate, StartupResponse
from app.startups.service import create_startup, get_startup_by_user
from app.startups.credibility import calculate_credibility
from app.startups.credibility_schemas import CredibilityOut

router = APIRouter(prefix="/startups", tags=["startups"])

@router.post("/", response_model=StartupResponse)
def create_my_startup(
    payload: StartupCreate,
    db: Session = Depends(get_db),
    user=Depends(require_role("startup")),
):
    # Persist user if not exists
    db_user = get_or_create_user(
        db,
        clerk_user_id=user["user_id"],
        email=user.get("email", "unknown@example.com"),
        role=user["role"],
    )

    # Enforce one startup per user
    existing = get_startup_by_user(db, db_user.id)
    if existing:
        raise HTTPException(status_code=400, detail="Startup already exists")

    return create_startup(db, db_user.id, payload)


@router.get("/me", response_model=StartupResponse)
def get_my_startup(
    db: Session = Depends(get_db),
    user=Depends(require_role("startup")),
):
    db_user = get_or_create_user(
        db,
        clerk_user_id=user["user_id"],
        email=user.get("email", "unknown@example.com"),
        role=user["role"],
    )

    startup = get_startup_by_user(db, db_user.id)
    if not startup:
        raise HTTPException(status_code=404, detail="Startup not found")

    return startup


@router.get("/me/credibility", response_model=CredibilityOut)
def get_my_credibility(
    db: Session = Depends(get_db),
    user=Depends(require_role("startup")),
):
    db_user = get_or_create_user(
        db,
        clerk_user_id=user["user_id"],
        email=user.get("email", "unknown@example.com"),
        role=user["role"],
    )

    startup = get_startup_by_user(db, db_user.id)
    if not startup:
        raise HTTPException(status_code=404, detail="Startup not found")

    return calculate_credibility(db, startup)