from app.celery import celery_app  # Importar la instancia de Celery

@celery_app.task
def add(x, y):
    return x + y

@celery_app.task
def multiply(x, y):
    return x * y

@celery_app.task
def slow_operation(n):
    import time
    time.sleep(n)
    return f"Esperaste {n} segundos"
