# MITRA Database Migration Guide: SQLite → MySQL

This document provides a comprehensive guide for migrating the MITRA database from SQLite to MySQL as part of Phase 2 of MITRA 2.0.

## Overview

This migration:
- Replaces SQLite with MySQL 8.x as the primary relational database
- Implements Alembic for schema management
- Preserves all existing data
- Maintains API compatibility
- Establishes a foundation for future enhancements

## Current Architecture (Before Migration)

```
Streamlit
    ↓
FastAPI (Phase 1 architecture)
    ↓
Service Layer
    ↓
Repository Layer
    ↓
SQLAlchemy ORM
    ↓
SQLite Database
```

## Target Architecture (After Migration)

```
Streamlit
    ↓
FastAPI (Phase 1 architecture)
    ↓
Service Layer
    ↓
Repository Layer
    ↓
SQLAlchemy ORM
    ↓
MySQL 8.x Database
```

## Prerequisites

### 1. Install MySQL 8.x

Download and install MySQL 8.x from [https://dev.mysql.com/downloads/mysql/](https://dev.mysql.com/downloads/mysql/)

**On Ubuntu/Debian:**
```bash
sudo apt update
sudo apt install mysql-server
sudo systemctl start mysql
sudo systemctl enable mysql
```

**On macOS (with Homebrew):**
```bash
brew install mysql
brew services start mysql
```

**On Windows:**
Download and run the MySQL installer from the official website.

### 2. Create MySQL Database

Log in to MySQL and create the database:

```sql
mysql -u root -p
```

```sql
CREATE DATABASE mitra CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
CREATE USER 'mitra_user'@'localhost' IDENTIFIED BY 'your_secure_password';
GRANT ALL PRIVILEGES ON mitra.* TO 'mitra_user'@'localhost';
FLUSH PRIVILEGES;
EXIT;
```

### 3. Verify MySQL Installation

```bash
mysql -u mitra_user -p mitra
```

## Environment Configuration

### 1. Create `.env` File

Copy the example environment file:

```bash
cd backend
cp .env.example .env
```

### 2. Configure Database URL

Edit the `.env` file and set the `DATABASE_URL`:

```bash
# For MySQL (production)
DATABASE_URL=mysql+pymysql://mitra_user:your_secure_password@localhost:3306/mitra
```

**Important:**
- Replace `mitra_user` with your MySQL username
- Replace `your_secure_password` with your MySQL password
- Replace `mitra` with your database name if different
- Do NOT commit the `.env` file to version control

### 3. Install Dependencies

Ensure all dependencies are installed:

```bash
cd ..
pip install -r requirements.txt
```

The following dependencies are required for MySQL:
- `sqlalchemy>=2.0.25` - ORM
- `alembic>=1.12.0` - Database migrations
- `pymysql>=1.1.0` - MySQL driver
- `cryptography>=41.0.0` - Required by PyMySQL

## Database Schema Migration

### 1. Initialize Alembic (First Time Only)

If Alembic is not yet initialized:

```bash
cd backend
alembic init alembic
```

This should already be done in the project. The structure should be:

```
backend/
├── alembic/
│   ├── versions/
│   ├── env.py
│   └── script.py.mako
└── alembic.ini
```

### 2. Configure Alembic

The `alembic.ini` file is already configured to load the database URL from the application's configuration system.

The `alembic/env.py` file is configured to:
- Import the SQLAlchemy models from `app.database.models`
- Use the application's database configuration
- Support both SQLite and MySQL

### 3. Review Migration Scripts

The initial migration script is located at:
```
backend/alembic/versions/001_initial_schema.py
```

This migration creates:
- `admissions` table with indexes
- `courses` table with indexes
- `facilities` table with indexes
- `contact_info` table with indexes
- `qa_dataset` table with indexes

All tables use:
- `utf8mb4` character set for full Unicode support
- `utf8mb4_unicode_ci` collation for case-insensitive Unicode comparisons
- Appropriate indexes for common query patterns

### 4. Run Alembic Migrations

Apply the database schema to MySQL:

```bash
cd backend
alembic upgrade head
```

This will:
- Connect to MySQL using the `DATABASE_URL` from `.env`
- Execute the migration scripts
- Create all tables with proper schema
- Create indexes for performance

**Expected Output:**
```
INFO  [alembic.runtime.migration] Context impl MySQLImpl.
INFO  [alembic.runtime.migration] Will assume non-transactional DDL.
INFO  [alembic.runtime.migration] Running upgrade  -> 001_initial_schema
```

### 5. Verify Schema Creation

Log in to MySQL and verify the tables were created:

```sql
USE mitra;
SHOW TABLES;
```

Expected output:
```
+-----------------------+
| Tables_in_mitra       |
+-----------------------+
| admissions            |
| courses               |
| facilities            |
| contact_info          |
| qa_dataset            |
+-----------------------+
```

Check table structure:

```sql
DESCRIBE admissions;
DESCRIBE courses;
DESCRIBE facilities;
DESCRIBE contact_info;
DESCRIBE qa_dataset;
```

## Data Migration

### 1. Locate SQLite Database

The SQLite database is typically located at:
```
backend/data/knowledge_base/college_info.db
```

### 2. Backup SQLite Database

Before migration, create a backup:

```bash
cd backend
cp data/knowledge_base/college_info.db data/knowledge_base/college_info.db.backup
```

### 3. Run Data Migration Script

The project includes a migration script to transfer data from SQLite to MySQL:

```bash
cd backend
python scripts/migrate_sqlite_to_mysql.py
```

This script will:
- Read data from the SQLite database
- Validate each record
- Insert records into MySQL
- Preserve primary key IDs
- Handle NULL values correctly
- Handle Unicode correctly
- Report progress and any errors

**Expected Output:**
```
Starting SQLite → MySQL migration
Source database: data/knowledge_base/college_info.db
Target database: mysql+pymysql://mitra_user:***@localhost:3306/mitra

Migrating table: admissions
  Migrated 6 records

Migrating table: courses
  Migrated 4 records

Migrating table: facilities
  Migrated 3 records

Migrating table: contact_info
  Migrated 5 records

Migrating table: qa_dataset
  Migrated 10 records

Migration completed successfully
Total records migrated: 28
```

### 4. Verify Data Migration

Run the validation script:

```bash
cd backend
python scripts/validate_mysql_migration.py
```

This script will verify:
- Database connection
- Table existence
- Row counts match between SQLite and MySQL
- Primary key integrity
- Sample record integrity
- Unicode/text integrity
- Application-level database queries

**Expected Output:**
```
Starting migration validation
Source database: data/knowledge_base/college_info.db
Target database: mysql+pymysql://mitra_user:***@localhost:3306/mitra

✓ Database connection successful
✓ All required tables exist
✓ Row counts match:
  - admissions: 6 == 6
  - courses: 4 == 4
  - facilities: 3 == 3
  - contact_info: 5 == 5
  - qa_dataset: 10 == 10
✓ Primary key integrity verified
✓ Sample record integrity verified
✓ Unicode integrity verified
✓ Application queries successful

Migration validation: PASS
```

## Application Startup

### 1. Start the FastAPI Backend

```bash
cd backend
python -m app.main
```

The application will:
- Load configuration from `.env`
- Connect to MySQL
- Initialize database connectivity
- Start the FastAPI server

**Expected Output:**
```
INFO:     Started server process [12345]
INFO:     Waiting for application startup.
INFO:     Starting MITRA - AI Powered College Helpdesk Assistant in development mode
INFO:     Database URL: mysql+pymysql://mitra_user:***@localhost:3306/mitra
INFO:     Database connection established successfully: MySQL
INFO:     Application startup complete
INFO:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
```

### 2. Verify API Endpoints

Test the API endpoints:

```bash
# Health check
curl http://localhost:8000/health

# Get intents
curl http://localhost:8000/intents

# Get Q&A pairs
curl http://localhost:8000/qa
```

### 3. Start the Streamlit Frontend

In a new terminal:

```bash
cd streamlit_app
streamlit run main.py
```

The frontend will connect to the MySQL-backed API and function normally.

## Rollback Procedure

If the migration validation fails or you need to rollback to SQLite:

### 1. Stop the Application

Stop both the FastAPI backend and Streamlit frontend.

### 2. Switch Back to SQLite

Edit the `.env` file:

```bash
# For SQLite (rollback)
DATABASE_URL=sqlite:///./data/knowledge_base/college_info.db
```

### 3. Restart the Application

```bash
cd backend
python -m app.main
```

The application will use the original SQLite database.

### 4. Drop MySQL Tables (Optional)

If you want to clean up the MySQL database:

```sql
mysql -u mitra_user -p mitra
```

```sql
DROP TABLE IF EXISTS qa_dataset;
DROP TABLE IF EXISTS contact_info;
DROP TABLE IF EXISTS facilities;
DROP TABLE IF EXISTS courses;
DROP TABLE IF EXISTS admissions;
```

**Important:** The original SQLite database (`college_info.db`) is never modified during migration, so it remains available as a rollback option.

## Troubleshooting

### MySQL Connection Errors

**Error:** `Can't connect to MySQL server on 'localhost'`

**Solution:**
- Verify MySQL is running: `sudo systemctl status mysql` (Linux) or check Services (Windows)
- Verify the MySQL username and password in `.env`
- Verify the database name exists

**Error:** `Access denied for user 'mitra_user'@'localhost'`

**Solution:**
- Verify the user exists: `SELECT user FROM mysql.user;`
- Revoke and grant privileges if needed
- Check password is correct in `.env`

### Alembic Migration Errors

**Error:** `Target database is not up to date`

**Solution:**
- Check current migration status: `alembic current`
- Force upgrade: `alembic upgrade head`
- Check migration history: `alembic history`

### Data Migration Errors

**Error:** `Table 'admissions' doesn't exist`

**Solution:**
- Run Alembic migrations first: `alembic upgrade head`
- Verify tables exist in MySQL

**Error:** `UnicodeDecodeError`

**Solution:**
- Ensure MySQL database uses `utf8mb4` character set
- Recreate database with correct charset:
  ```sql
  DROP DATABASE mitra;
  CREATE DATABASE mitra CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
  ```

### Application Errors

**Error:** `ModuleNotFoundError: No module named 'pymysql'`

**Solution:**
- Install dependencies: `pip install -r requirements.txt`

**Error:** `sqlalchemy.exc.OperationalError`

**Solution:**
- Verify `DATABASE_URL` in `.env` is correct
- Verify MySQL is running
- Verify database exists

## Common Migration Errors

### 1. Auto-increment ID Conflicts

**Issue:** Migrated records have ID conflicts with auto-increment.

**Solution:** The migration script preserves IDs explicitly. If conflicts occur, reset auto-increment:

```sql
ALTER TABLE admissions AUTO_INCREMENT = (SELECT MAX(id) + 1 FROM admissions);
```

### 2. NULL Constraint Violations

**Issue:** MySQL rejects NULL values that SQLite allowed.

**Solution:** Check the SQLite database for NULL values and update the schema if needed. The current schema allows NULL where appropriate.

### 3. String Length Truncation

**Issue:** MySQL VARCHAR fields truncate long strings.

**Solution:** The migration uses appropriate VARCHAR lengths (255, 500, etc.) based on actual data. Adjust in models if needed.

### 4. Index Creation Failures

**Issue:** Index creation fails due to duplicate data.

**Solution:** The migration script checks for duplicates. If manual cleanup is needed:

```sql
SELECT category, COUNT(*) FROM admissions GROUP BY category HAVING COUNT(*) > 1;
```

## Testing

### Run Unit Tests

Unit tests use in-memory SQLite and should pass regardless of MySQL:

```bash
pytest tests/ -m unit -v
```

### Run Integration Tests

Integration tests can run against MySQL:

```bash
DATABASE_URL=mysql+pymysql://mitra_user:password@localhost:3306/mitra_test pytest tests/ -m integration -v
```

### Run MySQL-Specific Tests

```bash
DATABASE_URL=mysql+pymysql://mitra_user:password@localhost:3306/mitra_test pytest tests/ -m mysql -v
```

### Run All Tests

```bash
pytest tests/ -v
```

## Performance Considerations

### Connection Pooling

The MySQL connection uses connection pooling with these settings:
- `pool_pre_ping=True`: Verify connections before using
- `pool_recycle=3600`: Recycle connections after 1 hour
- `pool_size=5`: Maintain 5 connections
- `max_overflow=10`: Allow up to 10 additional connections

Adjust these in `backend/app/database/connection.py` based on your workload.

### Indexes

The following indexes are created for performance:
- `admissions.category`
- `courses.course_name`
- `courses.department`
- `facilities.facility_name`
- `facilities.category`
- `contact_info.department`
- `qa_dataset.question`

Review and add more indexes based on actual query patterns.

## Security Considerations

### Credentials

- Never commit `.env` file to version control
- Use strong passwords for MySQL users
- Restrict MySQL user privileges to the minimum required
- Use environment variables for all sensitive configuration

### Database Access

- Don't expose MySQL directly to the internet
- Use a firewall to restrict access
- Consider using SSL for MySQL connections in production
- Regularly update MySQL to the latest version

## Monitoring

### Log Files

Application logs are written to:
- Console (default)
- File (if configured in `app/core/logging.py`)

Monitor logs for:
- Database connection errors
- Slow queries
- Migration issues

### MySQL Performance

Monitor MySQL performance using:
```sql
SHOW PROCESSLIST;
SHOW ENGINE INNODB STATUS;
```

## Summary

This migration successfully:
- ✅ Replaces SQLite with MySQL 8.x
- ✅ Implements Alembic for schema management
- ✅ Preserves all existing data
- ✅ Maintains API compatibility
- ✅ Supports Unicode with utf8mb4
- ✅ Provides rollback capability
- ✅ Includes comprehensive testing

The MITRA application is now ready for production use with MySQL, providing better performance, scalability, and reliability compared to SQLite.
