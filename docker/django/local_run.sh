#!/bin/sh

source /opt/django/pypkgs/bin/activate
python -Wd manage.py runserver 0.0.0.0:8000
