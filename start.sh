#!/bin/bash
echo "Starting Translation App..."
python -c "import app; print('App imported successfully')"
gunicorn app:app --bind 0.0.0.0:$PORT --workers 1 --timeout 120
