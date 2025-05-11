import os
from celery import Celery

broker_url = os.environ.get("CELERY_BROKER_URL")
result_backend = os.environ.get("CELERY_RESULT_BACKEND")

celery = Celery(
    "tasks",
    broker=broker_url,
    backend=result_backend
)

@celery.task
def add(x, y):
    return x + y

@celery.task
def multiply(x, y):
    return x * y

@celery.task
def slow_operation(n):
    import time
    time.sleep(n)
    return f"Esperaste {n} segundos"