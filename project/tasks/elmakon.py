from services import get_all_categories

from elmakon.category import prog as elmakon_category
from elmakon.product import prog as elmakon_product


def parse_elmakon_category():
    try:
        elmakon_category()
    except Exception as e:
        print(f"Error in parse_elmakon_category: {e}")


def parse_elmakon_product():
    try:
        data = [category.url for category in get_all_categories(website="elmakon")]
        elmakon_product(data)
    except Exception as e:
        print(f"Error in parse_elmakon_product: {e}")
