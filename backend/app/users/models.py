from sqlalchemy import Column, String
from app.core.models import BaseModel

class User(BaseModel):
    __tablename__ = "users"

    clerk_user_id = Column(String, unique=True, index=True, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    role = Column(String, nullable=False)
