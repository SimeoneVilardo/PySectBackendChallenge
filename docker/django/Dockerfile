# This Dockerfile uses multi-stage build to customize DEV and PROD images:
# https://docs.docker.com/develop/develop-images/multistage-build/

FROM python:3.11-bullseye AS builder_image

LABEL maintainer="simeone.vilardo@gmail.com"
LABEL vendor="PySect"

ARG DJANGO_ENV

# user args
ARG USER=web
ARG USER_ID=1000
ARG USER_GID=1000

ENV DJANGO_ENV=${DJANGO_ENV} \
  # python:
  PYTHONFAULTHANDLER=1 \
  PYTHONUNBUFFERED=1 \
  PYTHONHASHSEED=random \
  PYTHONDONTWRITEBYTECODE=1

WORKDIR /code

# Setting up proper permissions:
RUN groupadd -r ${USER} --gid ${USER_GID} && useradd --uid ${USER_ID} -d /code -r -g ${USER} ${USER} \
  && chown ${USER}:${USER} -R /code \
  && mkdir -p /var/www/django/static /var/www/django/media \
  && chown ${USER}:${USER} /var/www/django/static /var/www/django/media

COPY --chown=${USER}:${USER} ./requirements.txt /code/

# Project initialization:
RUN mkdir -p /opt/django \
  && /bin/bash -c 'python -m venv /opt/django/pypkgs \
  && source /opt/django/pypkgs/bin/activate \
  && pip install -r requirements.txt'

ENV PATH="/opt/django/pypkgs/bin:$PATH"
RUN echo "source /opt/django/pypkgs/bin/activate" >> /root/.bashrc

# Cleanup with a new stage:
FROM python:3.11-bullseye as runner_image

ARG DJANGO_ENV

# user args
ARG USER=web
ARG USER_ID=1000
ARG USER_GID=1000

ENV DJANGO_ENV=${DJANGO_ENV} \
  PYTHONFAULTHANDLER=1 \
  PYTHONUNBUFFERED=1 \
  PYTHONHASHSEED=random \
  PYTHONDONTWRITEBYTECODE=1

COPY --from=builder_image /opt/django /opt/django

ENV PYTHONPATH=/opt/django/pypkgs/lib/python3.11/site-packages:/code/ \
  PATH=$PATH:/opt/django/pypkgs/bin/

WORKDIR /code

# Setting up proper permissions:
RUN groupadd -r ${USER} --gid ${USER_GID} && useradd --uid ${USER_ID} -d /code -r -g ${USER} ${USER} \
  && chown ${USER}:${USER} -R /code \
  && mkdir -p /var/www/django/static /var/www/django/media \
  && chown ${USER}:${USER} /var/www/django/static /var/www/django/media

# Copy code
COPY --chown=${USER}:${USER} . /code

# Running as non-root user:
USER $USER

# Expose django static files
VOLUME ["/code/storage/"]
VOLUME ["/var/www/django/static/"]
