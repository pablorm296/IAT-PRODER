#!/bin/bash

# Update repo
cd /srv/IAT
git pull

# Start python server
python /srv/IAT/Src/IAT/server.py

# Start ngninx
if [ "$1" = 'nginx' ]; then
    exec "$0"
else
    echo "Invalid entrypoint"
fi