from sqlalchemy import Column, String, Integer, Boolean, ForeignKey, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from app.core.models import BaseModel

class Launch(BaseModel):
    __tablename__ = "launches"

    startup_id = Column(UUID(as_uuid=True), ForeignKey("startups.id"), nullable=False)

    title = Column(String, nullable=False)
    tagline = Column(String, nullable=False)
    description = Column(Text, nullable=False)

    upvotes = Column(Integer, default=0)
    featured = Column(Boolean, default=False)

    startup = relationship("Startup", backref="launches")
