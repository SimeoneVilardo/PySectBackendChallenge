# This Dockerfile uses multi-stage build to customize DEV and PROD images:
# https://docs.docker.com/develop/develop-images/multistage-build/

FROM python:3.12-bullseye AS builder_image

LABEL maintainer="simeone.vilardo@gmail.com"
LABEL vendor="PySect"

ENV PYTHONFAULTHANDLER=1 \
  PYTHONUNBUFFERED=1 \
  PYTHONHASHSEED=random \
  PYTHONDONTWRITEBYTECODE=1

WORKDIR /code

COPY ./requirements.txt /code/

# Project initialization:
RUN mkdir -p /opt/django \
  && /bin/bash -c 'python -m venv /opt/django/pypkgs \
  && source /opt/django/pypkgs/bin/activate \
  && pip install -r requirements.txt'

ENV PATH="/opt/django/pypkgs/bin:$PATH"
RUN echo "source /opt/django/pypkgs/bin/activate" >> /root/.bashrc

# Cleanup with a new stage:
FROM python:3.12-alpine as runner_image

ENV PYTHONFAULTHANDLER=1 \
  PYTHONUNBUFFERED=1 \
  PYTHONHASHSEED=random \
  PYTHONDONTWRITEBYTECODE=1

COPY --from=builder_image /opt/django /opt/django

ENV PYTHONPATH=/opt/django/pypkgs/lib/python3.11/site-packages:/code/ \
  PATH=$PATH:/opt/django/pypkgs/bin/

WORKDIR /code

# Copy code
COPY . /code

# Expose django static files
VOLUME ["/code/storage/"]
VOLUME ["/var/www/django/static/"]
