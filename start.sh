#!/bin/bash
# start.sh — Starts the OpenEnv API server
# On HF Spaces only one port (7860) is exposed, so the FastAPI server is primary.
# Streamlit runs on 8501 as a bonus UI (not required for evaluation).

set -e

echo "Starting SecureMail OpenEnv API on port 7860..."
exec uvicorn server:app --host 0.0.0.0 --port 7860
