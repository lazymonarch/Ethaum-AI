from sqlalchemy import Column, Boolean, ForeignKey, Integer, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from app.core.models import BaseModel

class EnterpriseFeedback(BaseModel):
    __tablename__ = "enterprise_feedback"

    startup_id = Column(UUID(as_uuid=True), ForeignKey("startups.id"), nullable=False)
    enterprise_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    match_id = Column(UUID(as_uuid=True), nullable=True)

    rating = Column(Integer, nullable=False)  # 1–5
    content = Column(Text, nullable=False)

    verified = Column(Boolean, default=False)

    startup = relationship("Startup", backref="enterprise_feedback")
