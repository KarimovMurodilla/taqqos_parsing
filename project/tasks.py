from celery import shared_task

from services import get_all_categories
from texnomart.category import prog
from texnomart.product import thr_prog
from mediapark.category import prog as mediapark_category


@shared_task()
def parse_technomart_product():
    data = [[category.url, category.name] for category in get_all_categories()]
    thr_prog(data)


@shared_task()
def parse_technomart_category():
    prog()


@shared_task()
def parse_mediapark_category():
    mediapark_category()
