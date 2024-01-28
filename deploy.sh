#!/bin/bash

while [ "$#" -gt 0 ]; do
  case "$1" in
    -env)
      if [ -n "$2" ]; then
        ENVIRONMENT="$2"
        shift
      else
        echo "Error: -env requires a valid environment (dev or prod)" >&2
        exit 1
      fi
      ;;
    *)
      echo "Error: Unknown option: $1" >&2
      exit 1
      ;;
  esac
  shift
done

if [ -z "$ENVIRONMENT" ]; then
  echo "Error: Please provide the environment using -env option (dev or prod)" >&2
  exit 1
fi

if [ "$ENVIRONMENT" == "dev" ]; then
  DOCKER_COMPOSE_FILE="docker-compose.dev.yml"
  GIT_BRANCH="dev"
  WEB_CONTAINER="web-dev"
  PROJECT_NAME="pysect-backend-challenge-dev"
elif [ "$ENVIRONMENT" == "prod" ]; then
  DOCKER_COMPOSE_FILE="docker-compose.prod.yml"
  GIT_BRANCH="master"
  WEB_CONTAINER="web-prod"
  PROJECT_NAME="pysect-backend-challenge-prod"
else
  echo "Error: Unknown environment. Supported values are dev or prod." >&2
  exit 1
fi

BASE_DIR="/home/pi"
PROJECT_DIR="$BASE_DIR/$PROJECT_NAME"
cd "$PROJECT_DIR"

echo "Deploying to $ENVIRONMENT..."
echo "Shutting down containers..."
docker compose -f "$DOCKER_COMPOSE_FILE" down
wait

echo "Downloading new code..."
git checkout "$GIT_BRANCH"
wait
git fetch --all
wait
git pull origin "$GIT_BRANCH"
wait

echo "Starting new containers..."
docker compose -f "$DOCKER_COMPOSE_FILE" up --build -d
wait

echo "Doing migrations..."
docker compose -f "$DOCKER_COMPOSE_FILE" exec "$WEB_CONTAINER" python manage.py migrate
wait

echo "Up and running!"