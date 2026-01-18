from fastapi import Header, HTTPException, Depends
from jose import jwt
import requests
import os

# ─────────────────────────────
# Clerk config
# ─────────────────────────────
CLERK_ISSUER = os.getenv("CLERK_ISSUER")
if not CLERK_ISSUER:
    raise RuntimeError("CLERK_ISSUER environment variable is not set")

CLERK_JWKS_URL = f"{CLERK_ISSUER}/.well-known/jwks.json"

_jwks_cache = None


def get_jwks():
    global _jwks_cache
    if _jwks_cache is None:
        response = requests.get(CLERK_JWKS_URL, timeout=5)
        response.raise_for_status()
        _jwks_cache = response.json()
    return _jwks_cache


# ─────────────────────────────
# Auth: get current user
# ─────────────────────────────
def get_current_user(authorization: str = Header(None)):
    if not authorization:
        raise HTTPException(status_code=401, detail="Missing Authorization header")

    if not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Invalid Authorization header")

    token = authorization.replace("Bearer ", "")

    try:
        payload = jwt.decode(
            token,
            get_jwks(),
            algorithms=["RS256"],
            issuer=CLERK_ISSUER,
            options={"verify_aud": False},
        )
    except Exception:
        raise HTTPException(status_code=401, detail="Invalid or expired token")

    role = payload.get("role")
    if not role:
        raise HTTPException(
            status_code=403,
            detail="User role missing in JWT",
        )

    clerk_user_id = payload.get("sub")
    if not clerk_user_id:
        raise HTTPException(
            status_code=401,
            detail="Invalid token: subject missing",
        )

    return {
        # 🔑 External identity ONLY
        "clerk_user_id": clerk_user_id,
        "email": payload.get("email"),
        "role": role,
    }


# ─────────────────────────────
# Auth: role guard
# ─────────────────────────────
def require_role(required_role: str):
    def role_checker(user=Depends(get_current_user)):
        if user["role"] != required_role:
            raise HTTPException(
                status_code=403,
                detail=f"Requires role: {required_role}",
            )
        return user

    return role_checker
