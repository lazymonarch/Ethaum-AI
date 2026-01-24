from sqlalchemy import Column, String
from sqlalchemy.orm import relationship

from app.core.database import Base  


class User(Base):
    __tablename__ = "users"

    id = Column(
        String,  
        primary_key=True,
    )

    clerk_user_id = Column(String, unique=True, index=True, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    role = Column(String, nullable=False)

    # 🔗 One-to-one Enterprise Profile
    enterprise_profile = relationship(
        "EnterpriseProfile",
        back_populates="user",
        uselist=False,
        foreign_keys="EnterpriseProfile.user_id",
        cascade="all, delete-orphan",
    )
