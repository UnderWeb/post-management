#!/bin/sh
set -e

echo "Waiting for SQL Server..."

until python - <<'PY'
import os
import pyodbc

server = os.getenv("DB_HOST", "db")
port = os.getenv("DB_PORT", "1433")
user = os.getenv("DB_USER", "sa")
password = os.getenv("DB_PASSWORD")

connection = (
    f"DRIVER={{ODBC Driver 18 for SQL Server}};"
    f"SERVER={server},{port};"
    "DATABASE=master;"
    f"UID={user};"
    f"PWD={password};"
    "TrustServerCertificate=yes;"
)

try:
    conn = pyodbc.connect(connection, timeout=5)
    conn.close()
    exit(0)
except Exception:
    exit(1)
PY
do
    echo "SQL Server not ready..."
    sleep 3
done

echo "SQL Server ready."

echo "Ensuring database exists..."

python - <<'PY'
import os
import pyodbc

server = os.getenv("DB_HOST", "db")
port = os.getenv("DB_PORT", "1433")
user = os.getenv("DB_USER", "sa")
password = os.getenv("DB_PASSWORD")
database = os.getenv("DB_NAME", "posts_db")

connection = (
    f"DRIVER={{ODBC Driver 18 for SQL Server}};"
    f"SERVER={server},{port};"
    "DATABASE=master;"
    f"UID={user};"
    f"PWD={password};"
    "TrustServerCertificate=yes;"
)

conn = pyodbc.connect(connection, autocommit=True)

cursor = conn.cursor()

cursor.execute(
    f"""
    IF DB_ID('{database}') IS NULL
    BEGIN
        CREATE DATABASE [{database}]
    END
    """
)

cursor.close()
conn.close()

PY

echo "Database ready."

echo "Running migrations..."
alembic upgrade head

echo "Running seeders..."
python scripts/seed.py

echo "Starting API..."

RELOAD_FLAG=""
if [ "${APP_ENV}" = "development" ]; then
    RELOAD_FLAG="--reload"
    echo "Hot-reload enabled."
fi

exec uvicorn app.main:app \
    --host "${HOST:-0.0.0.0}" \
    --port "${PORT:-8000}" \
    ${RELOAD_FLAG}
