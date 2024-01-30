import os

from celery import Celery
from celery.schedules import crontab

redis_url = os.environ.get("REDIS_URL", "redis://localhost:6379")

app = Celery(
    __name__,
    broker=redis_url,
    backend=redis_url,
    include=["tasks"]
)
app.conf.enable_utc = True
app.conf.timezone = "UTC"


app.conf.beat_schedule = {
    # Executes every Monday morning at 7:00 a.m.
    'parse-texnomart-product': {
        'task': 'tasks.parse_technomart_product',
        'schedule': crontab(hour='0', minute=20),
    },
    'parse-texnomart-category': {
        'task': 'tasks.parse_technomart_category',
        'schedule': crontab(),
    },

    'parse-elmakon-category': {
        'task': 'tasks.parse_elmakon_category',
        'schedule': crontab(),
    },
    'parse-elmakon-product': {
        'task': 'tasks.parse_elmakon_product',
        'schedule': crontab(hour='0', minute=20),
    },

    'parse-mediapark-product': {
        'task': 'tasks.parse_mediapark_product',
        'schedule': crontab(hour='0', minute=20),
    },
    'parse-mediapark-category': {
        'task': 'tasks.parse_mediapark_category',
        'schedule': crontab(),
    }
}

#hour=7, minute=0, day_of_week=1