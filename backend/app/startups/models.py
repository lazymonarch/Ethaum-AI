from sqlalchemy import Column, String, Integer, ForeignKey, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from app.core.models import BaseModel
from app.users.models import User

class Startup(BaseModel):
    __tablename__ = "startups"

    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)

    name = Column(String, nullable=False)
    industry = Column(String, nullable=False)
    arr_range = Column(String, nullable=False)
    description = Column(Text, nullable=False)

    credibility_score = Column(Integer, default=0)
    user = relationship(User, backref="startup")
