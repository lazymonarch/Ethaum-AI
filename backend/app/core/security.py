from fastapi import Header, HTTPException, Depends
from clerk_backend_api import Clerk
from app.core.config import CLERK_SECRET_KEY

if not CLERK_SECRET_KEY:
    raise RuntimeError("CLERK_SECRET_KEY is not set")

clerk = Clerk(bearer_auth=CLERK_SECRET_KEY)

def get_current_user(authorization: str = Header(None)):
    if not authorization:
        raise HTTPException(status_code=401, detail="Missing Authorization header")

    token = authorization.replace("Bearer ", "")
    session = clerk.verify_token(token)

    return {
        "user_id": session["sub"],
        "role": session.get("public_metadata", {}).get("role"),
    }


def require_role(required_role: str):
    def role_checker(user=Depends(get_current_user)):
        if user["role"] != required_role:
            raise HTTPException(
                status_code=403,
                detail=f"Requires role: {required_role}"
            )
        return user

    return role_checker
