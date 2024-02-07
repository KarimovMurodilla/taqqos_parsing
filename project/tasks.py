from celery import shared_task

from services import get_all_categories

from elmakon.category import prog as elmakon_category
from elmakon.product import prog as elmakon_product

from texnomart.category import prog as texnomart_category
from texnomart.product import prog as texnomart_product

from mediapark.category import prog as mediapark_category
from mediapark.product import prog as mediapark_product

from openshop.category import prog as openshop_category
from openshop.product import prog as openshop_product

from allgood.category import prog as allgood_category
from allgood.product import prog as allgood_product

from asaxiy.category import prog as asaxiy_category
from asaxiy.product import prog as asaxiy_product

from goodzone.category import prog as goodzone_category
from goodzone.product import prog as goodzone_product

from radius.category import prog as radius_category
from radius.product import prog as radius_product

from idea.category import prog as idea_category
from idea.product import prog as idea_product


@shared_task()
def parse_texnomart_category():
    texnomart_category()


@shared_task()
def parse_texnomart_product():
    data = [category.url for category in get_all_categories(website="texnomart")]
    texnomart_product(data)


@shared_task()
def parse_elmakon_category():
    elmakon_category()


@shared_task()
def parse_elmakon_product():
    data = [category.url for category in get_all_categories(website="elmakon")]
    elmakon_product(data)


@shared_task()
def parse_mediapark_category():
    mediapark_category()


@shared_task()
def parse_mediapark_product():
    data = [category.url for category in get_all_categories(website="mediapark")]
    mediapark_product(data)


@shared_task()
def parse_openshop_category():
    openshop_category()


@shared_task()
def parse_openshop_product():
    links = [category.url for category in get_all_categories(website="openshop")]
    openshop_product(links)


@shared_task()
def parse_allgood_category():
    allgood_category()


@shared_task()
def parse_allgood_product():
    links = [category.url for category in get_all_categories(website="allgood")]
    allgood_product(links)


@shared_task()
def parse_asaxiy_category():
    asaxiy_category()


@shared_task()
def parse_asaxiy_product():
    links = [category.url for category in get_all_categories(website="asaxiy")]
    asaxiy_product(links)


@shared_task()
def parse_goodzone_category():
    goodzone_category()


@shared_task()
def parse_goodzone_product():
    links = [category.url for category in get_all_categories(website="goodzone")]
    goodzone_product(links)


@shared_task()
def parse_radius_category():
    radius_category()


@shared_task()
def parse_radius_product():
    links = [category.url for category in get_all_categories(website="radius")]
    radius_product(links)


@shared_task()
def parse_idea_category():
    idea_category()


@shared_task()
def parse_idea_product():
    links = [category.url for category in get_all_categories(website="idea")]
    idea_product(links)