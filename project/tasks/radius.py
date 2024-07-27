from services import get_all_categories

from radius.category import prog as radius_category
from radius.product import prog as radius_product


def parse_radius_category():
    try:
        radius_category()
    except Exception as e:
        print(f"Error in parse_radius_category: {e}")


def parse_radius_product():
    try:
        data = [category.url for category in get_all_categories(website="radius")]
        radius_product(data)
    except Exception as e:
        print(f"Error in parse_radius_product: {e}")
