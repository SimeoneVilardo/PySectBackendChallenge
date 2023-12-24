FROM python:3.11-bullseye

ENV PYTHONUNBUFFERED 1

WORKDIR /code

# Copy requirements.txt
COPY docker/celery/requirements.txt /code/

# Install the specified packages
RUN pip install --no-cache-dir -r requirements.txt

# Set the CMD to your handler (could also be done as a parameter override outside of the Dockerfile)
CMD [ "celery -A server worker -l INFO" ]
