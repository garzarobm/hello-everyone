#!/bin/bash
set -e

# Fix ownership of data directory for bind mounts
# This runs as root before dropping to the 'may' user
if [ -d "/app/data" ]; then
    chown -R may:may /app/data
fi

# Create uploads directory if it doesn't exist
mkdir -p /app/data/uploads
chown -R may:may /app/data

# Run database migrations as the may user. Failures are logged rather than
# silently swallowed so upgrade problems are visible in container logs.
if ! gosu may flask db upgrade; then
    echo "[entrypoint] flask db upgrade failed — the app will attempt schema recovery on startup." >&2
fi

# Drop to 'may' user and run the application
exec gosu may "$@"
