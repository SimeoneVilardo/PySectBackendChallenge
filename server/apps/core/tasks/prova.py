from celery import shared_task
from server.celery import app

@app.task
def add(x, y):
    return x + y