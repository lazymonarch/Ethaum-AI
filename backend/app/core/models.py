import uuid
from sqlalchemy import Column, DateTime
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
from app.users.models import User
from app.enterprises.models import EnterpriseProfile
from app.core.database import Base


class BaseModel(Base):
    """
    Abstract base model for all database tables.

    Provides:
    - UUID primary key
    - created_at timestamp
    """
    __abstract__ = True

    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        index=True,
    )

    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )
