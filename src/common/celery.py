from celery import Celery
from src.common.configs import settings

app = Celery(
    'adebohost',
    broker=settings.redis.get_url(),
    backend=settings.redis.get_url(),
    include=['src.transaction.celery_tasks']
)

app.conf.update(result_expires=3600)
