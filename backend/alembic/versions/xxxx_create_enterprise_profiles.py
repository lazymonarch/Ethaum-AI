"""create enterprise_profiles table

Revision ID: e1_create_enterprise_profiles
Revises: b80584a4c461
Create Date: 2026-01-20
"""

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = "e1_create_enterprise_profiles"
down_revision = "b80584a4c461"
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        "enterprise_profiles",
        sa.Column(
            "id",
            postgresql.UUID(as_uuid=True),
            primary_key=True,
            nullable=False,
        ),
        sa.Column(
            "user_id",
            postgresql.UUID(as_uuid=True),
            sa.ForeignKey("users.id", ondelete="CASCADE"),
            nullable=False,
            unique=True,
        ),
        sa.Column("company_name", sa.String(), nullable=False),
        sa.Column("industry", sa.String(), nullable=False),
        sa.Column("company_size", sa.String(), nullable=False),
        sa.Column("location", sa.String(), nullable=False),

        sa.Column(
            "interested_industries",
            postgresql.ARRAY(sa.String()),
            nullable=False,
        ),
        sa.Column(
            "preferred_arr_ranges",
            postgresql.ARRAY(sa.String()),
            nullable=False,
        ),

        sa.Column("engagement_stage", sa.String(), nullable=True),

        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.func.now(),
            nullable=False,
        ),
        sa.Column(
            "updated_at",
            sa.DateTime(timezone=True),
            server_default=sa.func.now(),
            nullable=False,
        ),
    )


def downgrade():
    op.drop_table("enterprise_profiles")
