@echo off
cd /d "C:\Program Files\PostgreSQL\16\bin"
echo Changing directory to PostgreSQL bin folder...
echo.

set PGPASSWORD=SET_YOUR_PASSWORD_HERE

echo Dropping existing PostgreSQL database if it exists...
echo.
psql -U postgres -c "DROP DATABASE IF EXISTS songbirdb;"
echo.

echo Dropping existing PostgreSQL database if it exists...
echo.
psql -U postgres -c "CREATE USER songbird WITH PASSWORD 'songbird';"
echo.

echo Creating PostgreSQL database...
echo.
psql -U postgres -c "CREATE DATABASE songbirdb OWNER songbird;"
echo.

echo Creating PostgreSQL database...
echo.
psql -U postgres -c "ALTER USER songbird CREATEDB;"
echo.

echo PostgreSQL database created successfully.
