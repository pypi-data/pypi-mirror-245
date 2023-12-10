from celery import Celery

from .config.settings import CelerySettings
from .db import init_db
from .tasks.etl_task import start_task

app = Celery("app", broker=CelerySettings().rabbitmq_broker)


@app.task
@init_db
def run_etl_task(pages: list):
    return start_task(pages)
