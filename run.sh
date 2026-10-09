#!/bin/bash

# Exit immediately if a command exits with a non-zero status
set -e

echo "Seeding database with dummy products..."
uv run python seed.py

echo "Starting FastAPI server..."
uv run uvicorn app.main:app --host 127.0.0.1 --port 8000 --reload
