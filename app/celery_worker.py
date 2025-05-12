from app.celery import celery

celery.worker_main(["worker", "--loglevel=info"])