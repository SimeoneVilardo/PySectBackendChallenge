#!/bin/bash

# Startup code for django server used by the docker-compose.

source /opt/django/pypkgs/bin/activate
python -Wd manage.py runserver 0.0.0.0:8000
readonly cmd="$*"
exec $cmd
