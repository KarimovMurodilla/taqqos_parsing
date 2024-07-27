from services import get_all_categories

from goodzone.category import prog as goodzone_category
from goodzone.product import prog as goodzone_product


def parse_goodzone_category():
    try:
        goodzone_category()
    except Exception as e:
        print(f"Error in parse_goodzone_category: {e}")


def parse_goodzone_product():
    try:
        data = [category.url for category in get_all_categories(website="goodzone")]
        goodzone_product(data)
    except Exception as e:
        print(f"Error in parse_goodzone_product: {e}")
