from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.deps import get_db
from app.core.security import get_current_user, require_role
from app.users.service import get_or_create_user
from app.startups.service import get_startup_by_user
from app.launches.schemas import LaunchCreate, LaunchResponse
from app.launches.service import list_launches, upvote_launch
from app.launches.models import Launch

router = APIRouter(prefix="/launches", tags=["Launches"])


# -----------------------------------
# Create launch (startup only)
# -----------------------------------
@router.post(
    "/",
    response_model=LaunchResponse,
    dependencies=[Depends(require_role("startup"))],
)
def create_my_launch(
    launch: LaunchCreate,
    db: Session = Depends(get_db),
    user=Depends(get_current_user),
):
    # 1️⃣ Ensure user exists in DB
    db_user = get_or_create_user(
        db=db,
        clerk_user_id=user["clerk_user_id"],
        email=user["email"],
        role=user["role"],
    )

    # 2️⃣ Fetch startup owned by this user
    startup = get_startup_by_user(db, db_user.id)
    if not startup:
        raise HTTPException(status_code=404, detail="Startup not found")

    # 3️⃣ Create launch
    db_launch = Launch(
        startup_id=startup.id,
        title=launch.title,
        tagline=launch.tagline,
        description=launch.description,
        upvotes=0,
        featured=False,
    )

    db.add(db_launch)
    db.commit()
    db.refresh(db_launch)

    return db_launch


# -----------------------------------
# Get launches for current startup
# -----------------------------------
@router.get(
    "/me",
    response_model=list[LaunchResponse],
    dependencies=[Depends(require_role("startup"))],
)
def get_my_launches(
    db: Session = Depends(get_db),
    user=Depends(get_current_user),
):
    db_user = get_or_create_user(
        db=db,
        clerk_user_id=user["clerk_user_id"],
        email=user["email"],
        role=user["role"],
    )

    startup = get_startup_by_user(db, db_user.id)
    if not startup:
        return []  # 👈 empty state, not error

    return db.query(Launch).filter_by(startup_id=startup.id).all()


# -----------------------------------
# Public launches (enterprise view)
# -----------------------------------
@router.get("/", response_model=list[LaunchResponse])
def get_public_launches(db: Session = Depends(get_db)):
    return list_launches(db)


# -----------------------------------
# Upvote launch
# -----------------------------------
@router.post("/{launch_id}/upvote", response_model=LaunchResponse)
def upvote(
    launch_id: str,
    db: Session = Depends(get_db),
    user=Depends(get_current_user),
):
    db_user = get_or_create_user(
        db=db,
        clerk_user_id=user["clerk_user_id"],   # ✅ FIXED
        email=user["email"],
        role=user["role"],
    )

    try:
        return upvote_launch(db, launch_id, db_user.id)
    except ValueError:
        raise HTTPException(status_code=400, detail="Already upvoted")
