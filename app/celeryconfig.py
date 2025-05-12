# Serialización de tareas y resultados
task_serializer = "json"
accept_content = ["json"]
result_serializer = "json"

# Zona horaria
timezone = "UTC"
enable_utc = True

# Configuraciones del broker y backend
# Estas se configuran desde variables de entorno en celery.py,
# pero podemos definir opciones adicionales si es necesario
broker_connection_retry_on_startup = True
broker_connection_timeout = 10

# Configuraciones para resultados
result_backend_always_retry = True
result_expires = 3600  # Resultados expiran después de 1 hora

# Otras configuraciones útiles
task_track_started = True  # Rastrear cuando una tarea comienza
task_ignore_result = False  # Guardar resultados en el backend