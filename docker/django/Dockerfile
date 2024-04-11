# This Dockerfile uses multi-stage build to customize DEV and PROD images:
# https://docs.docker.com/develop/develop-images/multistage-build/

FROM python:3.11-bullseye AS builder_image

LABEL maintainer="simeone.vilardo@gmail.com"
LABEL vendor="PySect"

# user args
ARG USER=web

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
FROM python:3.11-bullseye as runner_image

# user args
ARG USER=web

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

# Running as non-root user:
USER $USER

# Expose django static files
VOLUME ["/code/storage/"]
VOLUME ["/var/www/django/static/"]
