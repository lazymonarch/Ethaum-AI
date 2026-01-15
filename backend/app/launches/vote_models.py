from sqlalchemy import Column, ForeignKey, UniqueConstraint
from sqlalchemy.dialects.postgresql import UUID
from app.core.models import BaseModel

class LaunchUpvote(BaseModel):
    __tablename__ = "launch_upvotes"

    launch_id = Column(UUID(as_uuid=True), ForeignKey("launches.id"), nullable=False)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)

    __table_args__ = (
        UniqueConstraint("launch_id", "user_id", name="unique_launch_upvote"),
    )
