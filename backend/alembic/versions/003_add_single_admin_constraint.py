"""Add single admin constraint using trigger

Revision ID: 003_add_single_admin_constraint
Revises: 002_add_users_table
Create Date: 2026-10-05 22:00:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '003_add_single_admin_constraint'
down_revision: Union[str, Sequence[str], None] = '002_add_users_table'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Add trigger to prevent multiple admin users."""
    # PostgreSQL trigger to prevent multiple admin users

    # Drop function if it exists (for idempotency)
    op.execute("""
        DROP FUNCTION IF EXISTS prevent_multiple_admins() CASCADE
    """)

    # Create function to check admin count
    op.execute("""
        CREATE OR REPLACE FUNCTION prevent_multiple_admins()
        RETURNS TRIGGER AS $$
        BEGIN
            IF NEW.is_admin = true THEN
                IF EXISTS (SELECT 1 FROM users WHERE is_admin = true) THEN
                    RAISE EXCEPTION 'Cannot create more than one administrator';
                END IF;
            END IF;
            RETURN NEW;
        END;
        $$ LANGUAGE plpgsql
    """)

    # Create trigger for inserts
    op.execute("""
        DROP TRIGGER IF EXISTS prevent_multiple_admins_insert ON users
    """)

    op.execute("""
        CREATE TRIGGER prevent_multiple_admins_insert
        BEFORE INSERT ON users
        FOR EACH ROW
        EXECUTE FUNCTION prevent_multiple_admins()
    """)

    # Create trigger for updates
    op.execute("""
        DROP TRIGGER IF EXISTS prevent_multiple_admins_update ON users
    """)

    op.execute("""
        CREATE TRIGGER prevent_multiple_admins_update
        BEFORE UPDATE ON users
        FOR EACH ROW
        WHEN (NEW.is_admin = true AND OLD.is_admin = false)
        EXECUTE FUNCTION prevent_multiple_admins()
    """)


def downgrade() -> None:
    """Remove single admin constraint triggers."""
    op.execute("""
        DROP TRIGGER IF EXISTS prevent_multiple_admins_insert ON users
    """)

    op.execute("""
        DROP TRIGGER IF EXISTS prevent_multiple_admins_update ON users
    """)

    op.execute("""
        DROP FUNCTION IF EXISTS prevent_multiple_admins() CASCADE
    """)
