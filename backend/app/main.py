from dotenv import load_dotenv
load_dotenv()

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi import Depends
from app.core.security import require_role
from app.startups.routes import router as startup_router
from app.launches.routes import router as launch_router
from app.reviews.routes import router as review_router
from app.feedback.routes import router as enterprise_feedback_router




app = FastAPI(title="EthAum.ai API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/health")
def health_check():
    return {"status": "ok"}

@app.get("/startup-only")
def startup_only(user=Depends(require_role("startup"))):
    return {"message": "Hello Startup User"}

@app.get("/enterprise-only")
def enterprise_only(user=Depends(require_role("enterprise"))):
    return {"message": "Hello Enterprise User"}

@app.get("/admin-only")
def admin_only(user=Depends(require_role("admin"))):
    return {"message": "Hello Admin User"}

app.include_router(startup_router)
app.include_router(launch_router)
app.include_router(review_router)
app.include_router(enterprise_feedback_router)