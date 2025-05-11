from celery import Celery
import os

celery = Celery(
    "tasks",
    broker=os.environ.get("CELERY_BROKER_URL"),
    backend=os.environ.get("CELERY_RESULT_BACKEND")
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
