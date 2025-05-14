from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from celery.result import AsyncResult
from app.tasks import add, multiply, slow_operation
from app.websockets import get_task_status

app = FastAPI()

@app.get("/")
async def root():
    return {"message": "Hello World"}

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
    elif task.state == "FAILURE":
        return {"task_id": task.id, "state": "Fallida", "result": str(task.result)}
    elif task.state == "RETRY":
        return {"task_id": task.id, "state": "Reintentando"}
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

# WebSocket endpoint para mantener la conexión abierta
@app.websocket("/ws/{task_id}")
async def websocket_endpoint(websocket: WebSocket, task_id: str):
    await websocket.accept()  # Aceptamos la conexión WebSocket
    try:
        while True:
            # Obtener el estado de la tarea y enviarlo al cliente
            status = await get_task_status(task_id)
            await websocket.send_text(f"Estado de la tarea {task_id}: {status}")
    except WebSocketDisconnect:
        print(f"Tarea {task_id} desconectada")
