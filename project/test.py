
# from pcmarket.category import parse_category
# from pcmarket.product import parse_product

from ikarvon.category import parse_category
from ikarvon.product import parse_product

from services import get_all_categories


if __name__ == '__main__':
    data = [category.url for category in get_all_categories(website="ikarvon")]

    parse_product(data)
