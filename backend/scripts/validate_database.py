"""Database validation script for MITRA production deployment.

This script performs read-only validation of the database to ensure:
- Database connection works
- MySQL version is compatible
- Required tables exist
- Required columns exist
- Primary keys exist
- Unique constraints exist
- Important indexes exist
- Users table exists with proper structure
- Exactly one admin exists after bootstrap
- Knowledge-base tables exist
- Row counts are available
- UTF-8/utf8mb4 configuration is correct

Usage:
    python scripts/validate_database.py
"""
import sys
import os

# Add backend to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from sqlalchemy import text, inspect
from app.database.connection import engine
from app.core.logging import logger


class DatabaseValidator:
    """Validates database structure and configuration."""

    def __init__(self):
        self.engine = engine
        self.issues = []
        self.warnings = []
        self.passed = []

    def log_issue(self, message: str):
        """Log a validation issue."""
        self.issues.append(message)
        logger.error(f"[ISSUE] {message}")

    def log_warning(self, message: str):
        """Log a validation warning."""
        self.warnings.append(message)
        logger.warning(f"[WARNING] {message}")

    def log_pass(self, message: str):
        """Log a passed validation."""
        self.passed.append(message)
        logger.info(f"[PASS] {message}")

    def validate_connection(self) -> bool:
        """Validate database connection."""
        try:
            with self.engine.connect() as conn:
                conn.execute(text("SELECT 1"))
            self.log_pass("Database connection successful")
            return True
        except Exception as e:
            self.log_issue(f"Database connection failed: {e}")
            return False

    def validate_mysql_version(self) -> bool:
        """Validate MySQL version is 8.x or higher."""
        try:
            with self.engine.connect() as conn:
                result = conn.execute(text("SELECT VERSION()"))
                version_str = result.scalar()
                version = float(version_str.split('.')[0] + '.' + version_str.split('.')[1])

                if version >= 8.0:
                    self.log_pass(f"MySQL version {version_str} is compatible (>= 8.0)")
                    return True
                else:
                    self.log_warning(f"MySQL version {version_str} is below recommended 8.0")
                    return True  # Not critical
        except Exception as e:
            self.log_warning(f"Could not check MySQL version: {e}")
            return True  # Not critical

    def validate_tables_exist(self) -> bool:
        """Validate all required tables exist."""
        required_tables = [
            'users',
            'admissions',
            'courses',
            'facilities',
            'contact_info',
            'qa_dataset'
        ]

        try:
            inspector = inspect(self.engine)
            existing_tables = inspector.get_table_names()

            all_exist = True
            for table in required_tables:
                if table in existing_tables:
                    self.log_pass(f"Table '{table}' exists")
                else:
                    self.log_issue(f"Required table '{table}' is missing")
                    all_exist = False

            return all_exist
        except Exception as e:
            self.log_issue(f"Failed to check table existence: {e}")
            return False

    def validate_users_table_structure(self) -> bool:
        """Validate users table has required columns."""
        required_columns = {
            'id': 'integer',
            'username': 'string',
            'email': 'string',
            'password_hash': 'string',
            'full_name': 'string',
            'is_active': 'boolean',
            'is_admin': 'boolean',
            'created_at': 'datetime',
            'updated_at': 'datetime',
            'last_login_at': 'datetime'
        }

        try:
            inspector = inspect(self.engine)
            columns = inspector.get_columns('users')

            column_names = {col['name'] for col in columns}
            all_exist = True

            for col_name, col_type in required_columns.items():
                if col_name in column_names:
                    self.log_pass(f"Column '{col_name}' exists in users table")
                else:
                    self.log_issue(f"Required column '{col_name}' is missing from users table")
                    all_exist = False

            return all_exist
        except Exception as e:
            self.log_issue(f"Failed to check users table structure: {e}")
            return False

    def validate_primary_keys(self) -> bool:
        """Validate primary keys exist on all tables."""
        required_tables = [
            'users',
            'admissions',
            'courses',
            'facilities',
            'contact_info',
            'qa_dataset'
        ]

        try:
            inspector = inspect(self.engine)
            all_exist = True

            for table in required_tables:
                pk = inspector.get_pk_constraint(table)
                if pk and pk.get('constrained_columns'):
                    self.log_pass(f"Primary key exists on table '{table}'")
                else:
                    self.log_issue(f"Primary key missing on table '{table}'")
                    all_exist = False

            return all_exist
        except Exception as e:
            self.log_issue(f"Failed to check primary keys: {e}")
            return False

    def validate_unique_constraints(self) -> bool:
        """Validate unique constraints on users table."""
        try:
            inspector = inspect(self.engine)
            uniques = inspector.get_unique_constraints('users')
            indexes = inspector.get_indexes('users')

            # Get unique columns from both unique constraints and unique indexes
            unique_columns = {col for u in uniques for col in u.get('constrained_columns', [])}
            for idx in indexes:
                if idx.get('unique', False):
                    unique_columns.update(idx.get('column_names', []))

            required_uniques = ['username', 'email']
            all_exist = True

            for col in required_uniques:
                if col in unique_columns:
                    self.log_pass(f"Unique constraint exists on users.{col}")
                else:
                    self.log_issue(f"Unique constraint missing on users.{col}")
                    all_exist = False

            return all_exist
        except Exception as e:
            self.log_issue(f"Failed to check unique constraints: {e}")
            return False

    def validate_indexes(self) -> bool:
        """Validate important indexes exist."""
        required_indexes = {
            'users': ['ix_users_username', 'ix_users_email', 'ix_users_is_admin', 'ix_users_is_active'],
            'courses': ['ix_courses_course_name', 'ix_courses_department'],
            'facilities': ['ix_facilities_facility_name', 'ix_facilities_category'],
            'admissions': ['ix_admissions_category'],
            'contact_info': ['ix_contact_info_department'],
            'qa_dataset': ['ix_qa_dataset_question']
        }

        try:
            inspector = inspect(self.engine)
            all_exist = True

            for table, indexes in required_indexes.items():
                table_indexes = [idx['name'] for idx in inspector.get_indexes(table)]
                for idx in indexes:
                    if idx in table_indexes:
                        self.log_pass(f"Index '{idx}' exists on table '{table}'")
                    else:
                        self.log_warning(f"Index '{idx}' missing on table '{table}' (recommended)")

            return all_exist
        except Exception as e:
            self.log_issue(f"Failed to check indexes: {e}")
            return False

    def validate_admin_count(self) -> bool:
        """Validate exactly one admin exists (if users table has data)."""
        try:
            with self.engine.connect() as conn:
                result = conn.execute(text("SELECT COUNT(*) FROM users WHERE is_admin = 1"))
                admin_count = result.scalar()

                if admin_count == 0:
                    self.log_warning("No admin user exists - run create_admin.py to bootstrap")
                elif admin_count == 1:
                    self.log_pass("Exactly one admin user exists")
                else:
                    self.log_issue(f"Multiple admin users exist ({admin_count}) - should be exactly one")

                return admin_count == 1
        except Exception as e:
            self.log_warning(f"Could not check admin count: {e}")
            return True  # Not critical if table doesn't exist yet

    def validate_row_counts(self) -> bool:
        """Validate row counts for knowledge-base tables."""
        tables = ['admissions', 'courses', 'facilities', 'contact_info', 'qa_dataset']

        try:
            with self.engine.connect() as conn:
                for table in tables:
                    result = conn.execute(text(f"SELECT COUNT(*) FROM {table}"))
                    count = result.scalar()
                    self.log_pass(f"Table '{table}' has {count} records")

            return True
        except Exception as e:
            self.log_warning(f"Could not check row counts: {e}")
            return True  # Not critical

    def validate_charset(self) -> bool:
        """Validate utf8mb4 charset configuration."""
        try:
            with self.engine.connect() as conn:
                result = conn.execute(text("SHOW VARIABLES LIKE 'character_set_database'"))
                charset = result.scalar()

                if charset and 'utf8mb4' in charset.lower():
                    self.log_pass(f"Database charset is {charset} (utf8mb4 compatible)")
                else:
                    self.log_warning(f"Database charset is {charset} (utf8mb4 recommended)")

                return True
        except Exception as e:
            self.log_warning(f"Could not check charset: {e}")
            return True  # Not critical

    def run_all_validations(self) -> bool:
        """Run all validation checks."""
        logger.info("=" * 60)
        logger.info("MITRA Database Validation")
        logger.info("=" * 60)

        self.validate_connection()
        self.validate_mysql_version()
        self.validate_tables_exist()
        self.validate_users_table_structure()
        self.validate_primary_keys()
        self.validate_unique_constraints()
        self.validate_indexes()
        self.validate_admin_count()
        self.validate_row_counts()
        self.validate_charset()

        logger.info("=" * 60)
        logger.info("Validation Summary")
        logger.info("=" * 60)
        logger.info(f"Passed: {len(self.passed)}")
        logger.info(f"Warnings: {len(self.warnings)}")
        logger.info(f"Issues: {len(self.issues)}")

        if self.issues:
            logger.error("VALIDATION FAILED - Issues found:")
            for issue in self.issues:
                logger.error(f"  - {issue}")
            return False

        if self.warnings:
            logger.warning("VALIDATION PASSED WITH WARNINGS:")
            for warning in self.warnings:
                logger.warning(f"  - {warning}")

        if not self.issues:
            logger.info("VALIDATION PASSED")
            return True

        return False


if __name__ == "__main__":
    validator = DatabaseValidator()
    success = validator.run_all_validations()
    sys.exit(0 if success else 1)
