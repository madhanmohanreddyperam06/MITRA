"""Initial schema for MITRA database

Revision ID: 001_initial_schema
Revises:
Create Date: 2026-10-05 19:35:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '001_initial_schema'
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Create initial schema for MITRA database."""
    # Create admissions table
    op.create_table(
        'admissions',
        sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
        sa.Column('category', sa.String(length=100), nullable=True),
        sa.Column('information', sa.String(length=255), nullable=True),
        sa.Column('details', sa.Text(), nullable=True),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index('ix_admissions_category', 'admissions', ['category'], unique=False)

    # Create courses table
    op.create_table(
        'courses',
        sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
        sa.Column('course_name', sa.String(length=255), nullable=True),
        sa.Column('department', sa.String(length=100), nullable=True),
        sa.Column('duration', sa.String(length=100), nullable=True),
        sa.Column('eligibility', sa.String(length=255), nullable=True),
        sa.Column('description', sa.Text(), nullable=True),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index('ix_courses_course_name', 'courses', ['course_name'], unique=False)
    op.create_index('ix_courses_department', 'courses', ['department'], unique=False)

    # Create facilities table
    op.create_table(
        'facilities',
        sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
        sa.Column('facility_name', sa.String(length=255), nullable=True),
        sa.Column('category', sa.String(length=100), nullable=True),
        sa.Column('description', sa.Text(), nullable=True),
        sa.Column('location', sa.String(length=255), nullable=True),
        sa.Column('timings', sa.String(length=100), nullable=True),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index('ix_facilities_facility_name', 'facilities', ['facility_name'], unique=False)
    op.create_index('ix_facilities_category', 'facilities', ['category'], unique=False)

    # Create contact_info table
    op.create_table(
        'contact_info',
        sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
        sa.Column('department', sa.String(length=100), nullable=True),
        sa.Column('contact_person', sa.String(length=255), nullable=True),
        sa.Column('phone', sa.String(length=50), nullable=True),
        sa.Column('email', sa.String(length=255), nullable=True),
        sa.Column('office_location', sa.String(length=255), nullable=True),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index('ix_contact_info_department', 'contact_info', ['department'], unique=False)

    # Create qa_dataset table
    op.create_table(
        'qa_dataset',
        sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
        sa.Column('question', sa.String(length=500), nullable=False),
        sa.Column('answer', sa.Text(), nullable=False),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index('ix_qa_dataset_question', 'qa_dataset', ['question'], unique=False)


def downgrade() -> None:
    """Drop all tables."""
    op.drop_index('ix_qa_dataset_question', table_name='qa_dataset')
    op.drop_table('qa_dataset')

    op.drop_index('ix_contact_info_department', table_name='contact_info')
    op.drop_table('contact_info')

    op.drop_index('ix_facilities_category', table_name='facilities')
    op.drop_index('ix_facilities_facility_name', table_name='facilities')
    op.drop_table('facilities')

    op.drop_index('ix_courses_department', table_name='courses')
    op.drop_index('ix_courses_course_name', table_name='courses')
    op.drop_table('courses')

    op.drop_index('ix_admissions_category', table_name='admissions')
    op.drop_table('admissions')
