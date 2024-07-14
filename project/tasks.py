import asyncio
import logging
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
from idea.product import main as idea_product


logging.basicConfig(level=logging.ERROR, format='%(asctime)s %(levelname)s %(message)s')


@shared_task()
def parse_texnomart_category():
    try:
        texnomart_category()
    except Exception as e:
        logging.error(f"Error in parse_texnomart_category: {e}")

@shared_task()
def parse_texnomart_product():
    try:
        data = [category.url for category in get_all_categories(website="texnomart")]
        texnomart_product(data)
    except Exception as e:
        logging.error(f"Error in parse_texnomart_product: {e}")

@shared_task()
def parse_elmakon_category():
    try:
        elmakon_category()
    except Exception as e:
        logging.error(f"Error in parse_elmakon_category: {e}")

@shared_task()
def parse_elmakon_product():
    try:
        data = [category.url for category in get_all_categories(website="elmakon")]
        elmakon_product(data)
    except Exception as e:
        logging.error(f"Error in parse_elmakon_product: {e}")

@shared_task()
def parse_mediapark_category():
    try:
        mediapark_category()
    except Exception as e:
        logging.error(f"Error in parse_mediapark_category: {e}")

@shared_task()
def parse_mediapark_product():
    try:
        data = [category.url for category in get_all_categories(website="mediapark")]
        mediapark_product(data)
    except Exception as e:
        logging.error(f"Error in parse_mediapark_product: {e}")

@shared_task()
def parse_openshop_category():
    try:
        openshop_category()
    except Exception as e:
        logging.error(f"Error in parse_openshop_category: {e}")

@shared_task()
def parse_openshop_product():
    try:
        links = [category.url for category in get_all_categories(website="openshop")]
        openshop_product(links)
    except Exception as e:
        logging.error(f"Error in parse_openshop_product: {e}")

@shared_task()
def parse_allgood_category():
    try:
        allgood_category()
    except Exception as e:
        logging.error(f"Error in parse_allgood_category: {e}")

@shared_task()
def parse_allgood_product():
    try:
        links = [category.url for category in get_all_categories(website="allgood")]
        allgood_product(links)
    except Exception as e:
        logging.error(f"Error in parse_allgood_product: {e}")

@shared_task()
def parse_asaxiy_category():
    try:
        asaxiy_category()
    except Exception as e:
        logging.error(f"Error in parse_asaxiy_category: {e}")

@shared_task()
def parse_asaxiy_product():
    try:
        links = [category.url for category in get_all_categories(website="asaxiy")]
        asaxiy_product(links)
    except Exception as e:
        logging.error(f"Error in parse_asaxiy_product: {e}")

@shared_task()
def parse_goodzone_category():
    try:
        goodzone_category()
    except Exception as e:
        logging.error(f"Error in parse_goodzone_category: {e}")

@shared_task()
def parse_goodzone_product():
    try:
        links = [category.url for category in get_all_categories(website="goodzone")]
        goodzone_product(links)
    except Exception as e:
        logging.error(f"Error in parse_goodzone_product: {e}")

@shared_task()
def parse_radius_category():
    try:
        radius_category()
    except Exception as e:
        logging.error(f"Error in parse_radius_category: {e}")

@shared_task()
def parse_radius_product():
    try:
        for category in get_all_categories(website="radius"):
            radius_product(category.url)
    except Exception as e:
        logging.error(f"Error in parse_radius_product: {e}")

@shared_task()
def parse_idea_category():
    try:
        idea_category()
    except Exception as e:
        logging.error(f"Error in parse_idea_category: {e}")

@shared_task()
def parse_idea_product():
    try:
        asyncio.run(idea_product())
    except Exception as e:
        logging.error(f"Error in parse_idea_product: {e}")
