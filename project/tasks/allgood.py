from services import get_all_categories

from allgood.category import prog as allgood_category
from allgood.product import prog as allgood_product


def parse_allgood_category():
    try:
        allgood_category()
    except Exception as e:
        print(f"Error in parse_allgood_category: {e}")


def parse_allgood_product():
    try:
        data = [category.url for category in get_all_categories(website="allgood")]
        allgood_product(data)
    except Exception as e:
        print(f"Error in parse_allgood_product: {e}")
