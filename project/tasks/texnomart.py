from services import get_all_categories

from texnomart.category import prog as texnomart_category
from texnomart.product import prog as texnomart_product


def parse_texnomart_category():
    try:
        texnomart_category()
    except Exception as e:
        print(f"Error in parse_texnomart_category: {e}")


def parse_texnomart_product():
    try:
        data = [category.url for category in get_all_categories(website="texnomart")]
        texnomart_product(data)
    except Exception as e:
        print(f"Error in parse_texnomart_product: {e}")
