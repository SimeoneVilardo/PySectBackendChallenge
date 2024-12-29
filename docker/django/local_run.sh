#!/bin/sh

if [ -f /opt/django/pypkgs/bin/activate ]; then
    . /opt/django/pypkgs/bin/activate
    python -Wd manage.py runserver 0.0.0.0:8000
else
    echo "Virtual environment not found!"
    exit 1
fi
