from celery import Celery
import os

broker_url = os.environ.get("CELERY_BROKER_URL")
result_backend = os.environ.get("CELERY_RESULT_BACKEND")

# Agregamos parámetros para evitar el error SSL en entorno de prueba
if broker_url and broker_url.startswith("rediss://"):
    broker_url += "&ssl_cert_reqs=CERT_NONE&ssl_check_hostname=false"
if result_backend and result_backend.startswith("rediss://"):
    result_backend += "&ssl_cert_reqs=CERT_NONE&ssl_check_hostname=false"

celery_app = Celery(
    "tasks",
    broker=broker_url,
    backend=result_backend
)

celery_app.config_from_object("app.celeryconfig")
celery_app.autodiscover_tasks(["app.tasks"])
