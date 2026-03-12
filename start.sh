#!/bin/sh

echo "Waiting for database..."

sleep 5

echo "Running migrations..."
alembic upgrade head

echo "Running seeders..."
python -m app.seeder.categories_seeder

echo "🚀 Starting FastAPI..."
uvicorn app.main:app --host 0.0.0.0 --port 8000