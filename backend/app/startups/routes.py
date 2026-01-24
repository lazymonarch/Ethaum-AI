from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.deps import get_db
from app.core.security import get_current_user, require_role
from app.users.service import get_or_create_user
from app.startups.schemas import StartupCreate, StartupResponse
from app.startups.service import create_startup, get_startup_by_user
from app.startups.credibility import calculate_credibility
from app.startups.credibility_schemas import CredibilityOut
from app.users.service import get_or_create_user
from app.startups.service import get_all_startups
from app.startups.service import discover_startups
from app.core.security import require_role

router = APIRouter(prefix="/startups", tags=["startups"])

@router.post("/", response_model=StartupResponse)
def create_my_startup(
    payload: StartupCreate,
    db: Session = Depends(get_db),
    user=Depends(get_current_user),
):
    db_user = get_or_create_user(
        db,
        clerk_user_id=user["clerk_user_id"], 
        email=user["email"],
        role=user["role"],
    )


    # Enforce one startup per user
    existing = get_startup_by_user(db, db_user.id)
    if existing:
        raise HTTPException(status_code=400, detail="Startup already exists")

    return create_startup(db, db_user.id, payload)

@router.get("", response_model=list[StartupResponse])
def list_startups(
    db: Session = Depends(get_db),
    user=Depends(get_current_user),
):
    # Allow enterprise + admin to browse
    if user["role"] not in ("enterprise", "admin"):
        raise HTTPException(status_code=403, detail="Not authorized")

    return get_all_startups(db)


@router.get("/me", response_model=StartupResponse)
def get_my_startup(
    db: Session = Depends(get_db),
    user=Depends(get_current_user),
):
    db_user = get_or_create_user(
        db,
        clerk_user_id=user["clerk_user_id"],
        email=user["email"],
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
        clerk_user_id=user["clerk_user_id"],
        email=user.get("email", "unknown@example.com"),
        role=user["role"],
    )

    startup = get_startup_by_user(db, db_user.id)
    if not startup:
        raise HTTPException(status_code=404, detail="Startup not found")

    return calculate_credibility(db, startup)


@router.get("/discover", response_model=list[StartupResponse])
def discover_startups_endpoint(
    industry: str | None = None,
    arr_range: str | None = None,
    min_score: int | None = None,
    sort: str = "credibility",
    db: Session = Depends(get_db),
    user=Depends(require_role("enterprise")),
):
    return discover_startups(
        db=db,
        industry=industry,
        arr_range=arr_range,
        min_score=min_score,
        sort=sort,
    )