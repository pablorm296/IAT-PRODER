#!/bin/bash

# Start python server
python /srv/IAT/Src/IAT/server.py

# Stop nginx
service nginx restart

# Start ngninx
if [ "$1" = 'nginx' ]; then
    exec "$0"
else
    echo "Invalid entrypoint"
fi