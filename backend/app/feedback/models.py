from sqlalchemy import Column, Boolean, ForeignKey, Integer, Text, UniqueConstraint
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from app.core.models import BaseModel

class EnterpriseFeedback(BaseModel):
    __tablename__ = "enterprise_feedback"

    __table_args__ = (
        UniqueConstraint(
            "startup_id",
            "enterprise_id",
            name="uq_enterprise_feedback_once",
        ),
    )

    startup_id = Column(
        UUID(as_uuid=True),
        ForeignKey("startups.id", ondelete="CASCADE"),
        nullable=False,
    )

    enterprise_id = Column(
        UUID(as_uuid=True),
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
    )

    match_id = Column(UUID(as_uuid=True), nullable=True)

    rating = Column(Integer, nullable=False)  # 1–5
    content = Column(Text, nullable=False)

    verified = Column(Boolean, default=False, nullable=False)

    startup = relationship("Startup", backref="enterprise_feedback")
