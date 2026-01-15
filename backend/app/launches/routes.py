from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.deps import get_db
from app.core.security import require_role, get_current_user
from app.startups.service import get_startup_by_user
from app.users.service import get_or_create_user
from app.launches.schemas import LaunchCreate, LaunchResponse
from app.launches.service import create_launch, list_launches, upvote_launch

router = APIRouter(prefix="/launches", tags=["launches"])

@router.post("/", response_model=LaunchResponse)
def create_my_launch(
    payload: LaunchCreate,
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
        raise HTTPException(status_code=400, detail="Startup profile required")

    return create_launch(db, startup.id, payload)


@router.get("/", response_model=list[LaunchResponse])
def get_public_launches(db: Session = Depends(get_db)):
    return list_launches(db)


@router.post("/{launch_id}/upvote", response_model=LaunchResponse)
def upvote(
    launch_id: str,
    db: Session = Depends(get_db),
    user=Depends(get_current_user),
):
    db_user = get_or_create_user(
        db,
        clerk_user_id=user["user_id"],
        email=user.get("email", "unknown@example.com"),
        role=user["role"],
    )

    try:
        return upvote_launch(db, launch_id, db_user.id)
    except ValueError:
        raise HTTPException(status_code=400, detail="Already upvoted")
