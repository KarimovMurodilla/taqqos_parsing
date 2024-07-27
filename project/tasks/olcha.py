from services import get_all_categories

from olcha.category import prog as olcha_category
from olcha.product import prog as olcha_product


def parse_olcha_category():
    try:
        olcha_category()
    except Exception as e:
        print(f"Error in parse_olcha_category: {e}")


def parse_olcha_product():
    try:
        data = [category.url for category in get_all_categories(website="olcha")]
        olcha_product(data)
    except Exception as e:
        print(f"Error in parse_olcha_product: {e}")
