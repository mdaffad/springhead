#! /usr/bin/env bash
set -e

if [ -f env/.env.local ]; then
    export $(cat env/.env.local | grep -v '#' | awk '/=/ {print $1}')
fi

LOG_LEVEL=${LOG_LEVEL:-"debug"}
HOST=${HOST:-"0.0.0.0"}
PORT=${PORT:-8888}
# Start Uvicorn with live reload
echo "ASDASD"
exec uvicorn springhead.main:app --reload --host $HOST --port $PORT --log-level $LOG_LEVEL 