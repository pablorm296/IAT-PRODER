#!/bin/bash

# Start python server
python /srv/IAT/Src/IAT/server.py

# Stop nginx
service nginx stop

# Start ngninx
ngninx