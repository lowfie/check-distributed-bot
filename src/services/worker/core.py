from datetime import timedelta

from celery import Celery
from celery.schedules import schedule

from src.config import settings
from src.services.bot.tasks import SendDistributedStatisticTask

celery_app = Celery(__name__, broker=settings.REDIS_DSN)

celery_app.conf.timezone = "UTC"

statistic_task = celery_app.register_task(SendDistributedStatisticTask)


celery_app.conf.beat_schedule = {
    "send-statistic-every-4-hours": {
        "task": statistic_task.name,
        "schedule": schedule(run_every=timedelta(hours=4)),
        "args": (),
    },
}
