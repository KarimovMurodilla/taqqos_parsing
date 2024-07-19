from services import get_all_categories

from pcmarket.category import parse_category as pcmarket_category
from pcmarket.product import parse_product as pcmarket_product


def parse_pcmarket_category():
    try:
        pcmarket_category()
    except Exception as e:
        print(f"Error in parse_pcmarket_category: {e}")


def parse_pcmarket_product():
    try:
        print("----------Started pcmarket product parsing------")
        data = [category.url for category in get_all_categories(website="pcmarket")]
        pcmarket_product(data)
    except Exception as e:
        print(f"Error in parse_pcmarket_product: {e}")

