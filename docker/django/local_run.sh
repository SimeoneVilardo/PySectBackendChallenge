#!/bin/bash

# Startup code for django server used by the docker-compose.

source /opt/django/pypkgs/bin/activate
/opt/django/pypkgs/bin/daphne -b 0.0.0.0 -p 8000 server.asgi:application
readonly cmd="$*"
exec $cmd
