from services import get_all_categories

from ikarvon.category import parse_category as ikarvon_category
from ikarvon.product import parse_product as ikarvon_product


def parse_ikarvon_category():
    try:
        ikarvon_category()
    except Exception as e:
        print(f"Error in parse_ikarvon_category: {e}")


def parse_ikarvon_product():
    try:
        data = [category.url for category in get_all_categories(website="ikarvon")]
        ikarvon_product(data)
    except Exception as e:
        print(f"Error in parse_ikarvon_product: {e}")
