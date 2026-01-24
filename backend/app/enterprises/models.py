import uuid
from sqlalchemy import Column, String, DateTime, ForeignKey
from sqlalchemy.dialects.postgresql import UUID, ARRAY
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship

from app.core.database import Base


class EnterpriseProfile(Base):
    __tablename__ = "enterprise_profiles"

    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        nullable=False,
    )

    # 🔗 ONE-TO-ONE with users table (ONLY FK needed)
    user_id = Column(
        UUID(as_uuid=True),
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
        unique=True,
    )

    # 🏢 Company info
    company_name = Column(String, nullable=False)
    industry = Column(String, nullable=False)
    company_size = Column(String, nullable=False)
    location = Column(String, nullable=False)

    # 🎯 Discovery preferences
    interested_industries = Column(
        ARRAY(String),
        nullable=False,
    )
    preferred_arr_ranges = Column(
        ARRAY(String),
        nullable=False,
    )

    # 🔄 Buying intent / maturity
    engagement_stage = Column(String, nullable=True)

    # 🕒 Timestamps
    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )
    updated_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False,
    )

    # 🔁 ORM relationship
    user = relationship(
        "User",
        back_populates="enterprise_profile",
        foreign_keys=[user_id],
        uselist=False,
    )
