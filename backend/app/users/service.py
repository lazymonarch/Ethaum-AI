from sqlalchemy.orm import Session
from app.users.models import User


def get_or_create_user(
    db: Session,
    clerk_user_id: str,
    email: str,
    role: str,
):
    user = db.query(User).filter_by(clerk_user_id=clerk_user_id).first()
    if user:
        return user

    user = User(
        clerk_user_id=clerk_user_id,
        email=email,
        role=role,
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user
