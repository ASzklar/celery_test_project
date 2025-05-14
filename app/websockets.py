from fastapi import WebSocket
from typing import Dict
from celery.result import AsyncResult

# Diccionario para almacenar las conexiones activas de WebSocket
active_connections: Dict[str, WebSocket] = {}

# Endpoint para mantener la conexión WebSocket abierta
async def websocket_endpoint(websocket: WebSocket, client_id: str):
    await websocket.accept()  # Aceptamos la conexión
    active_connections[client_id] = websocket  # Guardamos la conexión
    try:
        while True:
            await websocket.receive_text()  # Mantener la conexión abierta
    except Exception as e:
        # Si la conexión se cierra, eliminamos la conexión activa
        del active_connections[client_id]
        print(f"Conexión cerrada para el cliente {client_id}: {e}")

# Función para obtener el estado de una tarea
async def get_task_status(task_id: str):
    task = AsyncResult(task_id)
    
    # Devuelve el estado de la tarea según su estado actual
    if task.state == "PENDING":
        return "Pendiente"
    elif task.state == "SUCCESS":
        return f"Completada: {task.result}"
    elif task.state == "FAILURE":
        return f"Fallida: {task.result}"
    elif task.state == "RETRY":
        return "Reintentando"
    else:
        return task.state
