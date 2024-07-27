from services import get_all_categories

from openshop.category import prog as openshop_category
from openshop.product import prog as openshop_product


def parse_openshop_category():
    try:
        openshop_category()
    except Exception as e:
        print(f"Error in parse_openshop_category: {e}")


def parse_openshop_product():
    try:
        data = [category.url for category in get_all_categories(website="openshop")]
        openshop_product(data)
    except Exception as e:
        print(f"Error in parse_openshop_product: {e}")
