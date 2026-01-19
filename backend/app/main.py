from dotenv import load_dotenv
load_dotenv()

from fastapi import FastAPI, Request, Depends
from fastapi.responses import Response
from fastapi.middleware.cors import CORSMiddleware

from app.core.security import require_role
from app.startups.routes import router as startup_router
from app.launches.routes import router as launch_router
from app.reviews.routes import router as review_router
from app.feedback.routes import router as enterprise_feedback_router
from app.credibility.routes import router as credibility_router


app = FastAPI(title="EthAum.ai API")

# ✅ MUST BE FIRST — stops auth from running on OPTIONS
@app.middleware("http")
async def allow_preflight(request: Request, call_next):
    if request.method == "OPTIONS":
        return Response(status_code=200)
    return await call_next(request)

# ✅ CORS (unchanged)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# --------------------
# Health check
# --------------------
@app.get("/health")
def health_check():
    return {"status": "ok"}

# --------------------
# Role test endpoints
# --------------------
@app.get("/startup-only")
def startup_only(user=Depends(require_role("startup"))):
    return {"message": "Hello Startup User"}

@app.get("/enterprise-only")
def enterprise_only(user=Depends(require_role("enterprise"))):
    return {"message": "Hello Enterprise User"}

@app.get("/admin-only")
def admin_only(user=Depends(require_role("admin"))):
    return {"message": "Hello Admin User"}

# --------------------
# App routes
# --------------------
app.include_router(startup_router)
app.include_router(launch_router)
app.include_router(review_router)
app.include_router(enterprise_feedback_router)
app.include_router(credibility_router)
