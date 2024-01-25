from celery import shared_task

from texnomart.category import get_all_categories, prog
from texnomart.product import thr_prog


@shared_task()
def parse_technomart_product():
    data = [[category.url, category.name] for category in get_all_categories()]
    thr_prog(data)


@shared_task()
def parse_technomart_category():
    prog()
