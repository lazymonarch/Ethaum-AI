from sqlalchemy import Column, String, Boolean, ForeignKey, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from app.core.models import BaseModel

class Review(BaseModel):
    __tablename__ = "reviews"

    startup_id = Column(
        UUID(as_uuid=True),
        ForeignKey("startups.id"),
        nullable=False
    )

    user_id = Column(
        UUID(as_uuid=True),
        ForeignKey("users.id"),
        nullable=False
    )

    reviewer_role = Column(String, nullable=False)
    content = Column(Text, nullable=False)
    verified = Column(Boolean, default=False)

    startup = relationship("Startup", backref="reviews")
    user = relationship("User")
