from celery import Celery
import os

broker_url = os.environ.get("CELERY_BROKER_URL")
result_backend = os.environ.get("CELERY_RESULT_BACKEND")

celery_app = Celery(
    "tasks",
    broker=broker_url,
    backend=result_backend
)

celery_app.config_from_object("celeryconfig")

celery_app.autodiscover_tasks(["app.tasks"])
