from services import get_all_categories

from asaxiy.category import prog as asaxiy_category
from asaxiy.product import prog as asaxiy_product


def parse_asaxiy_category():
    try:
        asaxiy_category()
    except Exception as e:
        print(f"Error in parse_asaxiy_category: {e}")


def parse_asaxiy_product():
    try:
        data = [category.url for category in get_all_categories(website="asaxiy")]
        asaxiy_product(data)
    except Exception as e:
        print(f"Error in parse_asaxiy_product: {e}")
