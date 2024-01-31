from celery import shared_task

from services import get_all_categories

from elmakon.category import prog as elmakon_category
from elmakon.product import thr_prog as elmakon_product

from texnomart.category import prog as texnomart_category
from texnomart.product import thr_prog as texnomart_product
from mediapark.category import prog as mediapark_category
from mediapark.product import thr_prog as mediapark_product


@shared_task()
def parse_texnomart_category():
    texnomart_category()


@shared_task()
def parse_texnomart_product():
    data = [[category.url, category.name] for category in get_all_categories(website="texnomart")]
    texnomart_product(data, thr_ind=3)


@shared_task()
def parse_elmakon_category():
    elmakon_category()


@shared_task()
def parse_elmakon_product():
    data = [[category.url, category.name] for category in get_all_categories(website="elmakon")]
    elmakon_product(data, thr_ind=1)


@shared_task()
def parse_mediapark_category():
    mediapark_category()


@shared_task()
def parse_mediapark_product():
    data = [[category.url, category.name] for category in get_all_categories(website="mediapark")]
    mediapark_product(data, thr_ind=3)
