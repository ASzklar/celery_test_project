from fastapi import FastAPI
from celery.result import AsyncResult
from app.tasks import add, multiply, slow_operation
import time
import multiprocessing
import os
import app.celery

app = FastAPI()

@app.get("/")
async def root():
    return {"message": "Hola mundo"}

@app.get("/add_task/{x}/{y}")
async def add_task(x: int, y: int):
    task = add.apply_async(args=[x, y])
    return {"task_id": task.id, "message": "Tarea en cola"}

@app.get("/task_status/{task_id}")
async def task_status(task_id: str):
    task = AsyncResult(task_id)
    if task.state == "PENDING":
        return {"task_id": task.id, "state": "Pendiente"}
    elif task.state == "SUCCESS":
        return {"task_id": task.id, "state": "Completada", "result": task.result}
    else:
        return {"task_id": task.id, "state": task.state}

@app.get("/multiply_task/{x}/{y}")
async def multiply_task(x: int, y: int):
    task = multiply.apply_async(args=[x, y])
    return {"task_id": task.id, "message": "Tarea de multiplicación en cola"}

@app.get("/slow_task/{seconds}")
async def slow_task(seconds: int):
    task = slow_operation.apply_async(args=[seconds])
    return {"task_id": task.id, "message": f"Tarea lenta ({seconds}s) en cola"}

# Inicia Celery en un proceso aparte
def start_celery_worker():
    from celery import Celery
    celery_app = Celery('celery_test_project', broker=os.getenv("REDIS_URL"))
    celery_app.start()

# Inicia el proceso para Celery y luego inicia FastAPI
if __name__ == "__main__":
    p = multiprocessing.Process(target=start_celery_worker)
    p.start()
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)