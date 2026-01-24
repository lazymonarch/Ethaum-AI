"""enforce one feedback per enterprise per startup

Revision ID: 20bbe0158deb
Revises: e1_create_enterprise_profiles
Create Date: 2026-01-20 22:28:27.105979

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '20bbe0158deb'
down_revision: Union[str, Sequence[str], None] = 'e1_create_enterprise_profiles'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    op.create_unique_constraint(
        "uq_enterprise_feedback_once",
        "enterprise_feedback",
        ["startup_id", "enterprise_id"],
    )

def downgrade():
    op.drop_constraint(
        "uq_enterprise_feedback_once",
        "enterprise_feedback",
        type_="unique",
    )

