from app.celery import celery

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
