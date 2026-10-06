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
    # MySQL doesn't support partial indexes, so we use a trigger
    # This trigger will prevent creating a second admin user

    # Drop trigger if it exists (for idempotency)
    op.execute("""
        DROP TRIGGER IF EXISTS prevent_multiple_admins
    """)

    # Create trigger to prevent multiple admins
    op.execute("""
        CREATE TRIGGER prevent_multiple_admins
        BEFORE INSERT ON users
        FOR EACH ROW
        BEGIN
            DECLARE admin_count INT;
            IF NEW.is_admin = 1 THEN
                SELECT COUNT(*) INTO admin_count FROM users WHERE is_admin = 1;
                IF admin_count > 0 THEN
                    SIGNAL SQLSTATE '45000'
                    SET MESSAGE_TEXT = 'Cannot create more than one administrator';
                END IF;
            END IF;
        END
    """)

    # Also add trigger for updates
    op.execute("""
        DROP TRIGGER IF EXISTS prevent_multiple_admins_update
    """)

    op.execute("""
        CREATE TRIGGER prevent_multiple_admins_update
        BEFORE UPDATE ON users
        FOR EACH ROW
        BEGIN
            DECLARE admin_count INT;
            IF NEW.is_admin = 1 AND OLD.is_admin = 0 THEN
                SELECT COUNT(*) INTO admin_count FROM users WHERE is_admin = 1;
                IF admin_count > 0 THEN
                    SIGNAL SQLSTATE '45000'
                    SET MESSAGE_TEXT = 'Cannot have more than one administrator';
                END IF;
            END IF;
        END
    """)


def downgrade() -> None:
    """Remove single admin constraint triggers."""
    op.execute("""
        DROP TRIGGER IF EXISTS prevent_multiple_admins
    """)

    op.execute("""
        DROP TRIGGER IF EXISTS prevent_multiple_admins_update
    """)
