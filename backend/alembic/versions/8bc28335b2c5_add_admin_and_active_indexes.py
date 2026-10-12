"""add_admin_and_active_indexes

Revision ID: 8bc28335b2c5
Revises: 003_add_single_admin_constraint
Create Date: 2026-10-12 15:15:40.623721

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '8bc28335b2c5'
down_revision: Union[str, Sequence[str], None] = '003_add_single_admin_constraint'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Add indexes for is_admin and is_active columns."""
    # Create index for is_admin
    op.create_index('ix_users_is_admin', 'users', ['is_admin'], unique=False)

    # Create index for is_active
    op.create_index('ix_users_is_active', 'users', ['is_active'], unique=False)


def downgrade() -> None:
    """Remove indexes for is_admin and is_active columns."""
    # Drop index for is_active
    op.drop_index('ix_users_is_active', table_name='users')

    # Drop index for is_admin
    op.drop_index('ix_users_is_admin', table_name='users')
