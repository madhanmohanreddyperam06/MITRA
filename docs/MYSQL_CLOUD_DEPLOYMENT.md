# MITRA Cloud MySQL Deployment Guide

This document describes how to deploy MITRA with a Cloud MySQL database for production use.

## Table of Contents

1. [Supported MySQL Version](#supported-mysql-version)
2. [Cloud Database Configuration](#cloud-database-configuration)
3. [Creating the Cloud Database](#creating-the-cloud-database)
4. [Configuring DATABASE_URL](#configuring-database_url)
5. [SSL/TLS Configuration](#ssltls-configuration)
6. [Running Migrations](#running-migrations)
7. [Validating the Database](#validating-the-database)
8. [Creating the Single Admin](#creating-the-single-admin)
9. [Migrating Existing MITRA Data](#migrating-existing-mitra-data)
10. [Running the Backend](#running-the-backend)
11. [Running Streamlit](#running-streamlit)
12. [Verifying Authentication](#verifying-authentication)
13. [Verifying Guest Access](#verifying-guest-access)
14. [Verifying Admin Access](#verifying-admin-access)
15. [Backup Considerations](#backup-considerations)
16. [Production Security Considerations](#production-security-considerations)
17. [Troubleshooting](#troubleshooting)

---

## Supported MySQL Version

**Recommended: MySQL 8.x**

MITRA is tested and designed for MySQL 8.0 or higher. The database must support:
- utf8mb4 character set
- utf8mb4-compatible collation (e.g., utf8mb4_unicode_ci)
- Trigger support (for single admin constraint)
- Connection pooling
- Transaction support

---

## Cloud Database Configuration

### Recommended Cloud Providers

MITRA is compatible with any managed MySQL 8.x provider, including:

- **AWS RDS for MySQL**
- **Google Cloud SQL for MySQL**
- **Azure Database for MySQL**
- **PlanetScale**
- **DigitalOcean Managed Databases**
- **Railway**
- **Heroku Postgres** (not recommended - use MySQL)

### Database Requirements

- **Engine**: MySQL 8.0 or higher
- **Character Set**: utf8mb4
- **Collation**: utf8mb4_unicode_ci (or utf8mb4_0900_ai_ci)
- **Storage**: Minimum 10GB for production
- **Memory**: Minimum 2GB RAM
- **Connections**: Minimum 20 max connections

---

## Creating the Cloud Database

### Step 1: Provision the Database

1. Log in to your cloud provider's console
2. Create a new MySQL 8.x instance
3. Configure instance settings:
   - Set database name (e.g., `mitra_db`)
   - Create a dedicated database user
   - Generate a strong password
   - Set character set to utf8mb4
   - Enable automatic backups
   - Configure point-in-time recovery if available

### Step 2: Configure Network Access

1. Obtain the database host address
2. Configure firewall/security group rules:
   - Allow inbound connections from your application server
   - Restrict to specific IP addresses when possible
   - Use SSL/TLS if required by provider

### Step 3: Obtain Connection Details

You will need:
- **Host**: e.g., `mitra-db.xxxxx.us-east-1.rds.amazonaws.com`
- **Port**: typically `3306`
- **Database name**: e.g., `mitra_db`
- **Username**: database user name
- **Password**: database user password

---

## Configuring DATABASE_URL

### Format

```
mysql+pymysql://<username>:<password>@<host>:<port>/<database>
```

### Examples

**AWS RDS:**
```
DATABASE_URL=mysql+pymysql://mitra_user:SecurePass123@mitra-db.xxxxx.us-east-1.rds.amazonaws.com:3306/mitra_db
```

**Google Cloud SQL:**
```
DATABASE_URL=mysql+pymysql://mitra_user:SecurePass123@34.71.123.45:3306/mitra_db
```

**Azure Database for MySQL:**
```
DATABASE_URL=mysql+pymysql://mitra_user:SecurePass123@mitra-mysql.server.mysql.database.azure.com:3306/mitra_db
```

### Environment Configuration

1. Copy `.env.example` to `.env`
2. Set `DATABASE_URL` with your cloud database connection string
3. Set `APP_ENV=production`
4. Set `DEBUG=false`
5. Set a secure `JWT_SECRET_KEY`
6. Configure `CORS_ALLOWED_ORIGINS` with your frontend domain

**Never commit `.env` to Git.**

---

## SSL/TLS Configuration

### When SSL is Required

Some cloud providers require SSL/TLS connections. If your provider requires SSL:

### Option 1: Using SSL in Connection String

Add SSL parameters to the DATABASE_URL:

```
DATABASE_URL=mysql+pymysql://user:pass@host:3306/db?ssl_ca=/path/to/ca.pem&ssl_cert=/path/to/cert.pem&ssl_key=/path/to/key.pem
```

### Option 2: Using Environment Variables

For providers that use system CA certificates, no additional configuration is needed.

### Option 3: Disabling SSL (Not Recommended for Production)

Only for development:

```
DATABASE_URL=mysql+pymysql://user:pass@host:3306/db?ssl_disabled=true
```

---

## Running Migrations

### Step 1: Install Dependencies

```bash
cd backend
pip install -r requirements.txt
```

### Step 2: Set Environment Variables

```bash
export DATABASE_URL="mysql+pymysql://user:pass@host:3306/mitra_db"
export APP_ENV=production
```

Or use `.env` file.

### Step 3: Run Alembic Migrations

```bash
cd backend
alembic upgrade head
```

This will:
1. Create all required tables
2. Set up primary keys
3. Set up unique constraints
4. Create indexes
5. Add single admin constraint triggers

### Expected Output

```
INFO  [alembic.context] Running upgrade 001_initial_schema -> 002_add_users_table
INFO  [alembic.context] Running upgrade 002_add_users_table -> 003_add_single_admin_constraint
INFO  [alembic.context] Running upgrade 003_add_single_admin_constraint -> 8bc28335b2c5
```

---

## Validating the Database

### Run the Validation Script

```bash
cd backend
python scripts/validate_database.py
```

### What It Checks

1. ✅ Database connection works
2. ✅ MySQL version is compatible (>= 8.0)
3. ✅ Required tables exist (users, admissions, courses, facilities, contact_info, qa_dataset)
4. ✅ Required columns exist in users table
5. ✅ Primary keys exist
6. ✅ Unique constraints exist (username, email)
7. ✅ Important indexes exist
8. ⚠️ Exactly one admin exists (warning if 0)
9. ✅ Row counts are available
10. ✅ UTF-8/utf8mb4 configuration is correct

### Expected Output

```
============================================================
MITRA Database Validation
============================================================

[PASS] Database connection successful
[PASS] MySQL version 8.0.36 is compatible (>= 8.0)
[PASS] Table 'users' exists
[PASS] Table 'admissions' exists
[PASS] Table 'courses' exists
[PASS] Table 'facilities' exists
[PASS] Table 'contact_info' exists
[PASS] Table 'qa_dataset' exists
[PASS] Column 'id' exists in users table
[PASS] Column 'username' exists in users table
[PASS] Column 'email' exists in users table
[PASS] Column 'password_hash' exists in users table
[PASS] Column 'full_name' exists in users table
[PASS] Column 'is_active' exists in users table
[PASS] Column 'is_admin' exists in users table
[PASS] Column 'created_at' exists in users table
[PASS] Column 'updated_at' exists in users table
[PASS] Column 'last_login_at' exists in users table
[PASS] Primary key exists on table 'users'
[PASS] Unique constraint exists on users.username
[PASS] Unique constraint exists on users.email
[PASS] Index 'ix_users_username' exists on table 'users'
[PASS] Index 'ix_users_email' exists on table 'users'
[PASS] Index 'ix_users_is_admin' exists on table 'users'
[PASS] Index 'ix_users_is_active' exists on table 'users'
[WARNING] No admin user exists - run create_admin.py to bootstrap
[PASS] Table 'admissions' has 15 records
[PASS] Table 'courses' has 20 records
[PASS] Table 'facilities' has 12 records
[PASS] Table 'contact_info' has 8 records
[PASS] Table 'qa_dataset' has 50 records
[PASS] Database charset is utf8mb4 (utf8mb4 compatible)

============================================================
Validation Summary
============================================================
Passed: 34
Warnings: 1
Issues: 0

VALIDATION PASSED WITH WARNINGS:
  - No admin user exists - run create_admin.py to bootstrap
```

---

## Creating the Single Admin

### Step 1: Run the Admin Bootstrap Script

```bash
cd backend
python scripts/create_admin.py
```

### Step 2: Enter Admin Details

The script will prompt for:
- Admin username
- Admin email
- Admin password (hidden input)
- Confirm password
- Admin full name (optional)

### Step 3: Verification

The script will:
1. Check if an admin already exists
2. Refuse to create a second admin
3. Create the admin with `is_admin = true`
4. Securely hash the password
5. Commit the transaction

### Expected Output

```
============================================================
MITRA Administrator Setup
============================================================

Checking existing administrator...
No administrator exists. Proceeding with creation.

Please enter administrator details:
------------------------------------------------------------
Admin username: admin
Admin email: admin@mitra.edu
Admin password: ********
Confirm password: ********
Admin full name (optional): MITRA Administrator

------------------------------------------------------------
Creating administrator account...

============================================================
[SUCCESS] Administrator created successfully!
============================================================
Username: admin
Email: admin@mitra.edu
Full Name: MITRA Administrator

IMPORTANT: Your password has been securely hashed.
Please remember your password. It cannot be recovered.

You can now login to the application using these credentials.
============================================================
```

### Step 4: Validate Admin Creation

Run validation again:
```bash
python scripts/validate_database.py
```

Expected output should show:
```
[PASS] Exactly one admin user exists
```

---

## Migrating Existing MITRA Data

### If You Have Existing Data

If you have existing MITRA knowledge-base data in another database:

1. **Export from source database:**
   ```bash
   mysqldump -u source_user -p source_db admissions courses facilities contact_info qa_dataset > mitra_data.sql
   ```

2. **Import to cloud database:**
   ```bash
   mysql -u cloud_user -p cloud_host:3306/cloud_db < mitra_data.sql
   ```

3. **Run migrations:**
   ```bash
   alembic upgrade head
   ```

4. **Validate row counts:**
   ```bash
   python scripts/validate_database.py
   ```

### Data Validation

After migration, verify:
- Row counts match source
- Sample records are intact
- No duplicate records
- IDs are preserved where appropriate

---

## Running the Backend

### Step 1: Install Dependencies

```bash
cd backend
pip install -r requirements.txt
```

### Step 2: Configure Environment

```bash
export DATABASE_URL="mysql+pymysql://user:pass@host:3306/mitra_db"
export APP_ENV=production
export DEBUG=false
export JWT_SECRET_KEY="your-secure-random-secret"
export CORS_ALLOWED_ORIGINS="https://your-frontend-domain.com"
```

### Step 3: Start the Backend

```bash
cd backend
uvicorn app.main:app --host 0.0.0.0 --port 8000
```

Or using gunicorn for production:
```bash
gunicorn app.main:app -w 4 -k uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000
```

### Verify Backend Health

```bash
curl http://localhost:8000/health
```

Expected response:
```json
{
  "status": "healthy",
  "database": "connected"
}
```

---

## Running Streamlit

### Step 1: Install Dependencies

```bash
cd frontend
pip install -r requirements.txt
```

### Step 2: Configure Backend URL

Ensure Streamlit can reach the backend API. Update the API base URL in `components/auth.py` if needed.

### Step 3: Start Streamlit

```bash
cd frontend
streamlit run main.py
```

### Verify Frontend

Open browser to `http://localhost:8501` and verify:
- Landing page loads
- Registration works
- Login works
- Guest access works
- Authentication works

---

## Verifying Authentication

### Test Registration

```bash
curl -X POST http://localhost:8000/api/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "username": "testuser",
    "email": "test@example.com",
    "password": "TestPass123"
  }'
```

Expected response:
```json
{
  "id": 2,
  "username": "testuser",
  "email": "test@example.com",
  "full_name": null,
  "is_active": true,
  "is_admin": false,
  "created_at": "2026-10-12T...",
  "updated_at": "2026-10-12T...",
  "last_login_at": null
}
```

**Verify**: `is_admin` is always `false` for public registration.

### Test Login

```bash
curl -X POST http://localhost:8000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{
    "username_or_email": "testuser",
    "password": "TestPass123"
  }'
```

Expected response:
```json
{
  "access_token": "eyJ...",
  "token_type": "bearer"
}
```

### Test Current User

```bash
curl -X GET http://localhost:8000/api/auth/me \
  -H "Authorization: Bearer <token>"
```

Expected response should NOT include:
- `password_hash`
- `password`

---

## Verifying Guest Access

Guest access should work without authentication.

### Test Without Token

```bash
curl -X POST http://localhost:8000/api/chat \
  -H "Content-Type: application/json" \
  -d '{
    "message": "What courses are available?"
  }'
```

Guest users should be able to:
- Access public chatbot functionality
- Query knowledge base
- NOT access admin endpoints
- NOT access protected user data

---

## Verifying Admin Access

### Test Admin Login

```bash
curl -X POST http://localhost:8000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{
    "username_or_email": "admin",
    "password": "your-admin-password"
  }'
```

### Verify Admin Token

Use the admin token to access admin endpoints (if implemented).

Admin should be able to:
- Access all user functionality
- Access admin operations
- Manage users
- Manage knowledge base

---

## Backup Considerations

### Cloud Provider Backups

Most managed MySQL providers include:
- **Automated daily backups**
- **Point-in-time recovery (PITR)**
- **Manual snapshot capability**
- **Cross-region replication (optional)**

### Recommended Backup Strategy

1. **Enable automated backups** in your cloud provider console
2. **Set retention period** (e.g., 7-30 days)
3. **Test restore procedure** periodically
4. **Document backup schedule**
5. **Monitor backup success/failure**

### Manual Backup (Optional)

```bash
mysqldump -u user -p -h cloud-host mitra_db > backup_$(date +%Y%m%d).sql
```

---

## Production Security Considerations

### Environment Variables

- ✅ Use strong, randomly generated secrets
- ✅ Never commit `.env` to Git
- ✅ Use environment variable management for production
- ✅ Rotate secrets periodically
- ❌ Do not use default passwords
- ❌ Do not hardcode credentials

### Database Security

- ✅ Use strong database passwords
- ✅ Restrict network access (IP whitelisting)
- ✅ Enable SSL/TLS for connections
- ✅ Use least-privilege database users
- ✅ Monitor database access logs
- ❌ Do not expose database directly to internet

### Application Security

- ✅ Set `DEBUG=false` in production
- ✅ Use secure JWT secrets (32+ characters)
- ✅ Configure CORS to trusted origins only
- ✅ Use HTTPS for all API calls
- ✅ Implement rate limiting
- ❌ Do not log sensitive data

### Admin Security

- ✅ Admin created only through secure bootstrap script
- ✅ Admin password hashed with bcrypt
- ✅ Single admin constraint enforced at DB level
- ✅ Public registration cannot create admin
- ❌ Do not create admin automatically on startup
- ❌ Do not allow frontend to set `is_admin=true`

---

## Troubleshooting

### Connection Timeout

**Error**: `Can't connect to MySQL server on 'host' (timed out)`

**Solutions**:
1. Check database host is correct
2. Verify firewall/security group allows your IP
3. Check if database is running
4. Verify port (usually 3306)
5. Check if SSL is required

### Access Denied

**Error**: `Access denied for user 'user'@'ip'`

**Solutions**:
1. Verify username and password
2. Check user has permissions on the database
3. Verify host restrictions on user account
4. Check if user is allowed from your IP

### SSL Certificate Error

**Error**: `SSL certificate verification failed`

**Solutions**:
1. Download CA certificate from provider
2. Add `ssl_ca` parameter to DATABASE_URL
3. Or use `ssl_disabled=true` (not recommended for production)

### Migration Errors

**Error**: `Table already exists`

**Solutions**:
1. Check migration history: `alembic current`
2. If table exists but migration not recorded, mark as current: `alembic stamp head`
3. If migration failed, rollback: `alembic downgrade -1`
4. Re-run: `alembic upgrade head`

### Admin Creation Failed

**Error**: `Administrator already exists`

**Solutions**:
1. Check existing admin: `SELECT * FROM users WHERE is_admin = 1`
2. If admin exists, no action needed
3. If you need to reset admin, contact support
4. Never create a second admin

### UTF-8 Character Issues

**Error**: Characters not displaying correctly

**Solutions**:
1. Verify database charset is utf8mb4
2. Verify table charset is utf8mb4
3. Recreate database with correct charset if needed
4. Use validation script to check charset

### Performance Issues

**Symptoms**: Slow queries, connection timeouts

**Solutions**:
1. Check connection pool size (increase if needed)
2. Review indexes on frequently queried columns
3. Check database instance size (upgrade if needed)
4. Monitor slow query log
5. Use `EXPLAIN` to analyze slow queries

---

## Deployment Checklist

Before going to production:

- [ ] Cloud MySQL instance provisioned
- [ ] DATABASE_URL configured in environment
- [ ] APP_ENV set to production
- [ ] DEBUG set to false
- [ ] JWT_SECRET_KEY set to secure random value
- [ ] CORS_ALLOWED_ORIGINS configured
- [ ] Alembic migrations run successfully
- [ ] Database validation script passes
- [ ] Single admin created via bootstrap script
- [ ] Existing knowledge-base data migrated
- [ ] Backend starts successfully
- [ ] Health check endpoint responds
- [ ] Streamlit connects to backend
- [ ] Registration works
- [ ] Login works
- [ ] Guest access works
- [ ] Admin login works
- [ ] SSL/TLS configured (if required)
- [ ] Backups enabled
- [ ] Monitoring configured
- [ ] Log level set appropriately

---

## Support

For issues not covered in this guide:

1. Check the main project README
2. Review database provider documentation
3. Check Alembic documentation
4. Review SQLAlchemy documentation
5. Contact MITRA support channel

---

**Last Updated**: 2026-10-12
**Version**: 1.0
