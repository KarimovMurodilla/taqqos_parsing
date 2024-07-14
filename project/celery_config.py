import os

from celery import Celery
from celery.schedules import crontab

redis_url = os.environ.get("REDIS_URL", "redis://localhost:6379")

app = Celery(
    __name__,
    broker=redis_url,
    backend=redis_url,
    include=[
        "tasks",
        "maxcom.product",
        "maxcom.category",
        "pcmarket.product",
        "pcmarket.category",
        "ikarvon.category",
        "ikarvon.product",
    ]
)
app.conf.enable_utc = True
app.conf.timezone = "UTC"


app.conf.beat_schedule = {
    # Executes every Monday morning at 7:00 a.m.
    'parse-texnomart-product': {
        'task': 'tasks.parse_texnomart_product',
        'schedule': crontab(hour=6, minute=0),
    },
    'parse-texnomart-category': {
        'task': 'tasks.parse_texnomart_category',
        'schedule': crontab(hour=3, minute=40),
    },
    
    'parse-elmakon-product': {
        'task': 'tasks.parse_elmakon_product',
        'schedule': crontab(hour=5, minute=0),
    },
    'parse-elmakon-category': {
        'task': 'tasks.parse_elmakon_category',
        'schedule': crontab(hour=3, minute=40),
    },

    # 'parse-mediapark-product': {
    #     'task': 'tasks.parse_mediapark_product',
    #     'schedule': crontab(hour=0, minute=7),
    # },
    # 'parse-mediapark-category': {
    #     'task': 'tasks.parse_mediapark_category',
    #     'schedule': crontab(),
    # },

    # 'parse-openshop-product': {
    #     'task': 'tasks.parse_openshop_product',
    #     'schedule': crontab(hour=0, minute=24),
    # },
    # 'parse-openshop-category': {
    #     'task': 'tasks.parse_openshop_category',
    #     'schedule': crontab(),
    # },

    'parse-allgood-product': {
        'task': 'tasks.parse_allgood_product',
        'schedule': crontab(hour=6, minute=30),
    },
    'parse-allgood-category': {
        'task': 'tasks.parse_allgood_category',
        'schedule': crontab(hour=6, minute=10),
    },
    
    'parse-asaxiy-product': {
        'task': 'tasks.parse_asaxiy_product',
        'schedule': crontab(hour=6, minute=20),
    },
    'parse-asaxiy-category': {
        'task': 'tasks.parse_asaxiy_category',
        'schedule': crontab(hour=6, minute=10),
    },
    
    'parse-goodzone-product': {
        'task': 'tasks.parse_goodzone_product',
        'schedule': crontab(hour=6, minute=20),
    },
    'parse-goodzone-category': {
        'task': 'tasks.parse_goodzone_category',
        'schedule': crontab(hour=6, minute=10),
    },
    
    'parse-radius-product': {
        'task': 'tasks.parse_radius_product',
        'schedule': crontab(hour=6, minute=20),
    },
    'parse-radius-category': {
        'task': 'tasks.parse_radius_category',
        'schedule': crontab(hour=6, minute=10),
    },

    'parse-idea-product': {
        'task': 'tasks.parse_idea_product',
        'schedule': crontab(hour=11, minute=20),
    },
    'parse-idea-category': {
        'task': 'tasks.parse_idea_category',
        'schedule': crontab(hour=6, minute=10),
    }
}

#hour=7, minute=0, day_of_week=1